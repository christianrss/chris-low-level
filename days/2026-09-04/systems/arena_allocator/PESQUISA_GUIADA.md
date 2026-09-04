# Pesquisa guiada — Arena allocator

## Fonte de referência
Consulte cppreference, página **Objects and alignment** / `alignof` e `std::alignment_of`:
https://en.cppreference.com/w/cpp/language/object
https://en.cppreference.com/w/cpp/types/alignment_of

## Pesquise estes termos
- `C++ object alignment requirement`
- `power of two alignment bit mask`
- `arena allocator bump allocator`
- `std::pmr monotonic_buffer_resource` (apenas para comparação posterior)

## Responda antes de programar
1. Por que um `double` ou uma estrutura pode exigir alinhamento maior que 1?
2. O que significa um ponteiro estar alinhado em 32 bytes?
3. Qual a diferença entre *arena/bump allocator* e um allocator geral que permite `free` individual?
4. Por que `reset()` pode ser O(1)?
5. Em que situação `std::pmr::monotonic_buffer_resource` resolve problema parecido?

## Regra
Não copie implementação de allocator pronta. Use a documentação para validar conceitos; a implementação será construída abaixo.
