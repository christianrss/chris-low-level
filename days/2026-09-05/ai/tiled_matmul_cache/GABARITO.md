# Gabarito — AI — Matmul com Tiles e Cache

Respostas esperadas (consulte `solutions/` para código completo).

1. Naive: triplo loop i,j,k padrão.
2. trace_tile_4x4(5,7,4) → tile (1,1).
3. Tiled: loop em blocos ii,kk,jj com tile configurável.
4. Bench imprime tempos naive e tiled para N=128.
