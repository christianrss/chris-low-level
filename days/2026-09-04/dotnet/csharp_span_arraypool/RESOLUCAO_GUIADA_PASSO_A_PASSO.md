# Resolução guiada passo a passo

## Mapa exato starter → resolução

- `D2-CSHARP-WRITE-HEADER` → `starter/src/Chris.DotNet.Buffers/FrameCodec.cs`
- `D2-CSHARP-READ-HEADER` → `starter/src/Chris.DotNet.Buffers/FrameCodec.cs`
- `D2-CSHARP-RENT-FRAME` → `starter/src/Chris.DotNet.Buffers/FrameCodec.cs`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

## 0. Estrutura
Abra `starter/src/Chris.DotNet.Buffers/FrameCodec.cs`. O starter contém o projeto completo. Você vai editar somente os métodos marcados como TODO.

## 1. Fácil — gravar o header
Localize `FrameCodec.WriteHeader`.

Primeiro proteja o contrato:
```csharp
if (destination.Length < HeaderSize)
    throw new ArgumentException("destination is smaller than frame header", nameof(destination));
if (header.PayloadLength < 0)
    throw new ArgumentOutOfRangeException(nameof(header), "payload length cannot be negative");
```

Agora escreva cada campo na posição exata:
```csharp
BinaryPrimitives.WriteInt32LittleEndian(destination[0..4], header.PayloadLength);
BinaryPrimitives.WriteInt32LittleEndian(destination[4..8], header.MessageType);
```

Por que slices de quatro bytes? Um `Int32` ocupa 4 bytes; o segundo campo começa imediatamente depois do primeiro.

## 2. Médio — ler sem alocar
Em `ReadHeader`, valide `source.Length`, então use:
```csharp
var payloadLength = BinaryPrimitives.ReadInt32LittleEndian(source[0..4]);
var messageType = BinaryPrimitives.ReadInt32LittleEndian(source[4..8]);
```

Rejeite tamanho negativo antes de retornar:
```csharp
if (payloadLength < 0)
    throw new InvalidDataException("encoded payload length is negative");
return new FrameHeader(payloadLength, messageType);
```

## 3. Difícil — ownership com pool
Localize `RentFrame`.
```csharp
var required = checked(HeaderSize + payload.Length);
var buffer = ArrayPool<byte>.Shared.Rent(required);
WriteHeader(buffer.AsSpan(0, HeaderSize), new FrameHeader(payload.Length, messageType));
payload.CopyTo(buffer.AsSpan(HeaderSize, payload.Length));
return new PooledFrame(buffer, required);
```

### Leitura guiada do ownership já fornecido
`PooledFrame.Dispose` **já vem implementado no starter**. Leia-o e explique por que usa retorno único:
```csharp
var buffer = Interlocked.Exchange(ref _buffer, null);
if (buffer is not null)
    ArrayPool<byte>.Shared.Return(buffer, clearArray: false);
```

`Interlocked.Exchange` evita devolver o mesmo array duas vezes se `Dispose` for chamado repetidamente. Você não precisa editar `Dispose` neste exercício; o teste apenas valida o contrato observável de que `Memory` não pode ser usado depois do descarte.

## 4. Teste
```bash
dotnet run --project starter/tests/Chris.DotNet.Bench.Tests
```
Esperado:
```text
chris-dotnet-bench tests passed
```

## 5. Debugging
Breakpoint em `WriteHeader`. Observe `destination.Length`, `header.PayloadLength` e os oito bytes após as duas chamadas de `BinaryPrimitives`.

Se o payload sair deslocado, confira se você começou a cópia em `HeaderSize`, não em `0`.

Se aparecer `ObjectDisposedException`, verifique se alguma view está sendo usada depois de `Dispose`.

> Ambiente desta entrega: o SDK .NET não está instalado no container de validação. A estrutura/código foram revisados estaticamente, mas o comando acima deve ser executado em máquina com .NET 10 SDK; não trate esta entrega como evidência de execução local do C#.


## Solução final comentada
Depois de deixar o starter verde, compare somente os blocos `PEDAGOGY-SOLUTION` em `solutions/` correspondentes aos IDs do mapa. Se houver uma linha necessária no gabarito que não foi ensinada acima, trate como defeito do material e não como algo que você deveria adivinhar.
