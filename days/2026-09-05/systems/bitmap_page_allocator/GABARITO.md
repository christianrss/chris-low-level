# Gabarito — Systems — Alocador Bitmap de Páginas

Respostas esperadas (consulte `solutions/` para código completo).

1. Página 13 → byte 1, bit 5.
2. allocate percorre bits_ linearmente.
3. free_page retorna false se página já livre ou fora do range.
4. OOM: todas as páginas usadas, allocate retorna -1.
