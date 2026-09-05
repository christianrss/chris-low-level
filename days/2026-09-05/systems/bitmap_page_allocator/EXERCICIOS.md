# Exercícios — Systems — Alocador Bitmap de Páginas

Quatro níveis de dificuldade alinhados aos TODOs do módulo.

## Fácil
- **SYS-PAGE-ALLOC-01:** Implemente `trace_page_to_bit()` mapeando page→byte→bit.

## Médio
- **SYS-PAGE-ALLOC-01:** Implemente `allocate()` retornando primeira página livre.

## Difícil
- **SYS-PAGE-FREE-02:** Implemente `free_page()` rejeitando double-free e índice inválido.

## Expert
- **SYS-PAGE-ALLOC-01:** Explique OOM quando allocate retorna -1 e como escalar o bitmap.
