# Pesquisa guiada

Consulte documentação oficial do .NET sobre `Span<T>`, `Memory<T>`, `ArrayPool<T>`, `BinaryPrimitives` e `GC.GetAllocatedBytesForCurrentThread`.

Pesquise pelos termos:
- `site:learn.microsoft.com Span<T> ref struct`
- `site:learn.microsoft.com ArrayPool<T> Rent Return`
- `site:learn.microsoft.com BinaryPrimitives little endian`

Responda antes de implementar:
1. Por que `Span<T>` não pode ser armazenado em um objeto comum no heap?
2. O que pode acontecer se um buffer alugado for retornado e ainda existir uma referência para ele?
3. Quando `clearArray: true` pode ser necessário?
4. Por que medir apenas tempo sem medir allocations pode esconder um problema?

Use a documentação para entender contratos e tradeoffs; não copie a implementação interna do runtime.
