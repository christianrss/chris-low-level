# Testes guiados
1. Round-trip de `FrameHeader(1234,7)`.
2. `stackalloc byte[4]` deve ser rejeitado pelo writer.
3. Frame alugado deve conter header nos bytes 0..7 e payload a partir do byte 8.
4. Após `Dispose`, acessar `Memory` deve lançar `ObjectDisposedException`.

Rode:
```bash
dotnet run --project starter/tests/Chris.DotNet.Bench.Tests
```
No container desta entrega o SDK .NET não estava disponível; estes testes fazem parte do starter/solution, mas não foram executados localmente.
