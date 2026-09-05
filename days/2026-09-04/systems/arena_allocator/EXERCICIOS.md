# Exercícios — Arena allocator

## Fácil

- **D2-ARENA-POWER2:** implemente `is_power_of_two` em `starter/src/arena.cpp`. No caderno, prove manualmente para 1, 2, 3, 8, 16 e 0.
- Calcule no papel `align_up(0, 8)`, `align_up(13, 8)` e `align_up(24, 8)` antes de codificar.

## Médio

- **D2-ARENA-ALIGN-UP:** implemente `align_up` rejeitando alinhamentos que não são potência de dois com `std::invalid_argument`.
- Desenhe um diagrama de `storage_` com três alocações consecutivas mostrando padding entre elas.

## Difícil

- **D2-ARENA-ALLOCATE:** implemente `allocate` validando `size`, alinhando `base+offset`, checando capacidade sem overflow e avançando `offset_`.
- **D2-ARENA-RESET:** implemente `reset` em O(1) e explique por que ponteiros antigos ficam inválidos.

## Desafio

- Rode o benchmark com `-DCHRIS_BUILD_BENCHMARKS=ON` e compare arena versus alocações repetidas no heap. Escreva quando a comparação é justa e quando é enganosa (tamanho fixo, sem destruição, mesma thread).
- Proponha extensão `allocate_array<T>(count, alignment)` usando placement new e descreva o que falta para ser seguro em produção.
