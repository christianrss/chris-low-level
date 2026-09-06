# RESOLUÇÃO GUIADA — .NET / Span deflate buffers

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `DN-SPAN-01` | `starter/Program.cs` | `DeflateStored.ReadStoredHeader` |
| `DN-SPAN-02` | `starter/Program.cs` | `DeflateStored.InflateStored` (Slice/CopyTo) |
| `DN-SPAN-03` | `starter/Program.cs` | validação LEN/NLEN (+ truncamento payload) |

Cada ID existe como `TODO [ID]` no starter e `PEDAGOGY-SOLUTION` / `PEDAGOGY-TEST` no gabarito/`Program.cs`.

> Trabalhe em `days/2026-09-06/dotnet/span_deflate_buffers/starter/`. `solutions/` só depois.

> `BuildStoredBlock` e `Main` já estão prontos — implemente só `DeflateStored`.

---

## DN-SPAN-01 — ReadStoredHeader (BTYPE + offsets)

### 1. O problema (starter stub)

```csharp
public static int ReadStoredHeader(ReadOnlySpan<byte> input, out int dataOffset, out int length)
{
    // TODO [DN-SPAN-01]
    throw new NotImplementedException("DN-SPAN-01");
}
```

Sem header, `InflateStored` não tem como achar o payload.

### 2. O algoritmo

```text
se Length < 5 → InvalidDataException("truncated stored header")
BTYPE ← (input[0] >> 1) & 0x03
se BTYPE ≠ 0 → "not stored block"
LEN/NLEN LE16; (validação NLEN = DN-SPAN-03)
dataOffset ← 5; length ← LEN
return dataOffset
```

### 3. Código completo (header + DN-SPAN-03 juntos)

Implemente `ReadStoredHeader` assim (o gabarito une 01 e 03 no mesmo método):

```csharp
public static int ReadStoredHeader(ReadOnlySpan<byte> input, out int dataOffset, out int length)
{
    if (input.Length < 5)
    {
        throw new InvalidDataException("truncated stored header");
    }

    byte header = input[0];
    if (((header >> 1) & 0x03) != 0x00)
    {
        throw new InvalidDataException("not stored block");
    }

    ushort len = (ushort)(input[1] | (input[2] << 8));
    ushort nlen = (ushort)(input[3] | (input[4] << 8));
    if ((ushort)(len ^ nlen) != 0xFFFF)
    {
        throw new InvalidDataException("len/nlen mismatch");
    }

    dataOffset = 5;
    length = len;
    return dataOffset;
}
```

### 4. Por que funciona? (entenda linha a linha)

- `Length < 5`: não leia `input[4]` em buffer curto — o `Main` testa span de 3 bytes.
- `(header >> 1) & 0x03`: extrai BTYPE; para `0x01` → BTYPE=0 (stored). **Não** use `header & 0x03`.
- LEN/NLEN little-endian: byte baixo primeiro (`BuildStoredBlock` escreve assim).
- `(ushort)(len ^ nlen) != 0xFFFF`: complemento de um; cast `ushort` evita promoção signed estranha.
- `out` params: contrato usado por `InflateStored`.

### 5. Verificação parcial

Ainda não dá para `dotnet run` completo sem `InflateStored`. Você pode temporariamente só compilar; o próximo TODO fecha o loop.

---

## DN-SPAN-03 — LEN/NLEN (já no bloco acima)

### 1. O problema

O starter marca:

```csharp
// TODO [DN-SPAN-02]
// TODO [DN-SPAN-03]
```

em `InflateStored`, mas a checagem de complemento vive naturalmente em `ReadStoredHeader` (como no gabarito). Sem ela, um LEN corrompido aloca/copia tamanho errado.

### 2–4. Código e entendimento

Já incluídos na seção `DN-SPAN-01`. Critério: `len ^ nlen == 0xFFFF` como `ushort`.

Scratch mental para `"LOWLEVEL"`: `len=8`, `nlen=0xFFF7`, `8 ^ 0xFFF7 = 0xFFFF`.

---

## DN-SPAN-02 — InflateStored via Span

### 1. O problema (starter stub)

```csharp
public static byte[] InflateStored(ReadOnlySpan<byte> input)
{
    // TODO [DN-SPAN-02]
    // TODO [DN-SPAN-03]
    throw new NotImplementedException("DN-SPAN-02");
}
```

### 2. O algoritmo

```text
ReadStoredHeader(input, out dataOffset, out length)
se input.Length < dataOffset + length → InvalidDataException("truncated stored payload")
output ← new byte[length]
input.Slice(dataOffset, length).CopyTo(output)
retornar output
```

### 3. Código completo

```csharp
public static byte[] InflateStored(ReadOnlySpan<byte> input)
{
    int offset = ReadStoredHeader(input, out int dataOffset, out int length);
    if (input.Length < dataOffset + length)
    {
        throw new InvalidDataException("truncated stored payload");
    }

    var output = new byte[length];
    input.Slice(dataOffset, length).CopyTo(output);
    return output;
}
```

(`offset` fica igual a `dataOffset`; o gabarito mantém a variável — pode usar só `dataOffset`.)

### 4. Por que funciona? (entenda linha a linha)

- Reusa o header: uma única fonte de verdade para offset/LEN/NLEN.
- Segundo check: header ok mas payload cortado no meio (ex.: Length=6 com LEN=8).
- `Slice` + `CopyTo`: zero-copy no input; uma alocação na saída.
- `SequenceEqual` no `Main` compara com `"LOWLEVEL"u8`.

### 5. Verificação completa

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\dotnet\span_deflate_buffers\starter
dotnet run
```

Saída esperada:

```text
OK deflate stored
```

Gabarito:

```powershell
cd ..\solutions
dotnet run
```

Starter sem TODOs: `NotImplementedException`.

---

## Ordem sugerida

1. `ReadStoredHeader` completo (01+03).
2. `InflateStored` (02).
3. `dotnet run` — round-trip + truncado.
4. Compare com `solutions/Program.cs`.

## Relatório de resolução

### O que foi validado

- TODOs `DN-SPAN-01..03` em `starter/Program.cs`.
- `Main`: inflate `"LOWLEVEL"` ok; span de 3 bytes → `InvalidDataException`.
- BTYPE via `>> 1`; LEN/NLEN com XOR `0xFFFF`.

### Armadilhas encontradas

- Máscara BTYPE: shift obrigatório.
- Truncamento de header (`Length < 5`) vs truncamento de payload (`< dataOffset+length`) — dois throws distintos.
- Não alterar `BuildStoredBlock` (fixture canônico `0x01` + LE16).

### Depuração e saída esperada

- **Depuração:** imprima `input[0]`, `len`, `nlen` em hex; confira `08 00 F7 FF` para 8 bytes.
- **Saída esperada:** `OK deflate stored`.

### Próximo passo sugerido

Refazer sem olhar o gabarito. Em `BENCHMARK_GUIADO.md`, meça tempo de `InflateStored` em payloads 1 KiB / 64 KiB / 1 MiB (stored) versus `DeflateStream` se quiser contraste.
