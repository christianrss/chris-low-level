# RESOLUÇÃO GUIADA — .NET / Span, ArrayPool e frame binário

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `D2-CSHARP-WRITE-HEADER` | `starter/src/Chris.DotNet.Buffers/FrameCodec.cs` | `FrameCodec.WriteHeader` |
| `D2-CSHARP-READ-HEADER` | `starter/src/Chris.DotNet.Buffers/FrameCodec.cs` | `FrameCodec.ReadHeader` |
| `D2-CSHARP-RENT-FRAME` | `starter/src/Chris.DotNet.Buffers/FrameCodec.cs` | `FrameCodec.RentFrame` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-04/dotnet/csharp_span_arraypool/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

> Não comece copiando `solutions/`. Siga os passos abaixo e rode os testes a cada etapa.

Layout fixo do header (8 bytes):

```text
offset 0..3  PayloadLength  int32 little-endian
offset 4..7  MessageType    int32 little-endian
```

`PooledFrame.Dispose` **já vem implementado** no starter — leia-o; não o reescreva.

---

## Exercício Fácil — `D2-CSHARP-WRITE-HEADER`

### 1. O problema

O starter já valida destino e `PayloadLength`, mas o corpo do TODO só faz:

```csharp
destination[..HeaderSize].Clear();
```

O round-trip do teste grava `FrameHeader(1234, 7)` e espera ler de volta os mesmos campos. Com zeros, o decode falha.

### 2. O algoritmo

1. Confirme que as guards já existentes cobrem `destination.Length < HeaderSize` e `PayloadLength < 0`.
2. Escreva `PayloadLength` nos bytes `[0..4)`.
3. Escreva `MessageType` nos bytes `[4..8)`.
4. Use `BinaryPrimitives` em little-endian — o protocolo wire é LE, não o endian do host.

### 3. Escreva o código

Substitua o `Clear()` por:

```csharp
BinaryPrimitives.WriteInt32LittleEndian(destination[0..4], header.PayloadLength);
BinaryPrimitives.WriteInt32LittleEndian(destination[4..8], header.MessageType);
```

### 4. Por que funciona

Cada `Int32` ocupa exatamente 4 bytes. Slices `0..4` e `4..8` são views sobre o mesmo `Span<byte>` — **não alocam**. `BinaryPrimitives` fixa LE, então `1234` vira `D2 04 00 00` em qualquer máquina.

Trace manual `PayloadLength=100`, `MessageType=7`:

```text
64 00 00 00  07 00 00 00
```

### 5. Verifique

Ainda não rode o suite completo se `ReadHeader`/`RentFrame` estão vazios; confira visualmente com breakpoint ou um assert temporário nos 8 bytes. Critério parcial: após `WriteHeader`, `destination[0]==0xD2` e `destination[1]==0x04` para `1234`.

---

## Exercício Médio — `D2-CSHARP-READ-HEADER`

### 1. O problema

`ReadHeader` já rejeita `source` curto, mas o TODO deixa:

```csharp
var payloadLength = 0;
var messageType = 0;
```

O decode sempre devolve `(0, 0)`.

### 2. O algoritmo

Espelho de `WriteHeader`:

1. Leia LE nos mesmos slices.
2. Rejeite `payloadLength < 0` **depois** da leitura (o wire pode carregar lixo signed).
3. Retorne `new FrameHeader(payloadLength, messageType)`.

Não use `new byte[]`, `ToArray()`, nem `BitConverter` sem controlar endianness.

### 3. Escreva o código

```csharp
var payloadLength = BinaryPrimitives.ReadInt32LittleEndian(source[0..4]);
var messageType = BinaryPrimitives.ReadInt32LittleEndian(source[4..8]);
if (payloadLength < 0)
    throw new InvalidDataException("encoded payload length is negative");
return new FrameHeader(payloadLength, messageType);
```

(A checagem de `source.Length` já está acima do TODO no starter.)

### 4. Por que funciona

`ReadOnlySpan<byte>` é view; leitura in-place não toca o GC. Validar length negativo impede que um header malicioso force alocações enormes no próximo passo do pipeline (mesmo que este lab ainda não aloque pelo length).

### 5. Verifique

```bash
dotnet run --project starter/tests/Chris.DotNet.Bench.Tests
```

O round-trip `WriteHeader` → `ReadHeader` deve passar. `RentFrame` ainda pode falhar até o próximo exercício.

---

## Exercício Difícil — `D2-CSHARP-RENT-FRAME`

### 1. O problema

O starter aluga com `new byte[required]` e devolve `PooledFrame` **sem** gravar header nem copiar payload:

```csharp
var required = checked(HeaderSize + payload.Length);
var buffer = new byte[required];
return new PooledFrame(buffer, required);
```

Isso foge do objetivo: reutilizar `ArrayPool` e montar frame completo.

### 2. O algoritmo

```text
required = HeaderSize + payload.Length   (checked)
buffer   = ArrayPool<byte>.Shared.Rent(required)
WriteHeader(buffer[0..8], FrameHeader(payload.Length, messageType))
copiar payload para buffer[8 .. 8+payload.Length)
transferir ownership via new PooledFrame(buffer, required)
```

`checked` transforma overflow de tamanho em exceção em vez de buffer curto.

### 3. Escreva o código

```csharp
var required = checked(HeaderSize + payload.Length);
var buffer = ArrayPool<byte>.Shared.Rent(required);
WriteHeader(buffer.AsSpan(0, HeaderSize), new FrameHeader(payload.Length, messageType));
payload.CopyTo(buffer.AsSpan(HeaderSize, payload.Length));
return new PooledFrame(buffer, required);
```

### 4. Por que funciona — ownership

`Rent` pode devolver array **maior** que `required`. Por isso `PooledFrame` guarda `Length = required` e expõe `Memory` só até esse tamanho — bytes além de `required` não fazem parte do frame.

`Dispose` (já no starter):

```csharp
var buffer = Interlocked.Exchange(ref _buffer, null);
if (buffer is not null)
    ArrayPool<byte>.Shared.Return(buffer, clearArray: false);
```

`Exchange` zera o campo atomicamente: segundo `Dispose` vê `null` e não devolve duas vezes. Após dispose, `Memory` lança `ObjectDisposedException` — o teste cobre isso.

Armadilha clássica: copiar payload em offset `0` sobrescreve o header. Outra: usar `buffer.Length` (tamanho rentado) em vez de `required` como comprimento lógico.

### 5. Verifique

```bash
dotnet run --project starter/tests/Chris.DotNet.Bench.Tests
```

Esperado:

```text
chris-dotnet-bench tests passed
```

Checklist:

- [ ] Header do frame rentado decodifica `PayloadLength == payload.Length`
- [ ] Bytes `[8..]` batem com o payload
- [ ] Após `Dispose`, acessar `Memory` falha
- [ ] `WriteHeader` em span de 4 bytes lança

Benchmark (opcional):

```bash
dotnet run -c Release --project starter/benchmarks/Chris.DotNet.Bench.Benchmarks
```

Interprete com cuidado: `PooledFrame` ainda é um objeto gerenciado por operação; o ganho é no backing `byte[]`.

---

## Debugging

1. Breakpoint em `WriteHeader` — inspecione os 8 bytes após as duas escritas.
2. Se o payload sair “deslocado”, confira `CopyTo(..., HeaderSize)` e não `0`.
3. Se o teste de dispose passar mas o pool “vazar” em loops longos, confirme que todo `RentFrame` está em `using`.
4. Ambiente sem SDK .NET: revise estaticamente contra `solutions/`; execute localmente com .NET 10 SDK.

---

## Mapa de consistência auditada

- `D2-CSHARP-WRITE-HEADER` — `starter/.../FrameCodec.cs` → `solutions/.../FrameCodec.cs`
- `D2-CSHARP-READ-HEADER` — `starter/.../FrameCodec.cs` → `solutions/.../FrameCodec.cs`
- `D2-CSHARP-RENT-FRAME` — `starter/.../FrameCodec.cs` → `solutions/.../FrameCodec.cs`

Compare somente blocos `PEDAGOGY-SOLUTION` correspondentes. Se o gabarito exigir uma linha não ensinada acima, trate como defeito do material.

---

## Relatório de resolução

### O que foi validado

- `WriteHeader` / `ReadHeader` round-trip LE sem alocação.
- `RentFrame` usa `ArrayPool.Shared`, header em `[0..8)`, payload em `[8..)`.
- Dispose idempotente; `Memory` inválido após retorno ao pool.

### Armadilhas encontradas

- `BitConverter` sem LE explícito quebra em hosts big-endian (e obscurece o contrato).
- `Rent` length ≠ logical length — sempre publicar `required`.
- Double-`Return` sem `Interlocked` corrompe o pool compartilhado.

### Depuração e saída esperada

- **Depuração:** breakpoint nos slices; hex dos 8 bytes do header.
- **Saída esperada:** `chris-dotnet-bench tests passed`.

### Próximo passo sugerido

Rode o benchmark Release, registre alocações vs `new byte[]`, e anote em `BENCHMARK_GUIADO.md` o que *não* foi medido (I/O, multi-thread contention no `Shared` pool).
