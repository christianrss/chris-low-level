# Exercícios — Tiled matmul

## Fácil — AI-MM-NAIVE-01
Calcule manualmente C para A 2×2 e B 2×2 com valores inteiros pequenos.

## Médio — AI-MM-NAIVE-01
Implemente `matmul_naive()` até passar o teste da fixture 2×3·3×2.

## Médio — AI-MM-TILED-02
Implemente `trace_tile_4x4()` e verifique `(5,7,4) → tile (1,1)`.

## Difícil — AI-MM-TILED-02
Implemente `matmul_tiled()` e prove equivalência com naive em 3×5·5×4 com tile=2.

## Desafio
Rode benchmark em 256×256 com tiles 4, 8, 16 e plote mediana vs tile size.

## Reflexão
Por que tiling pode não ajudar (ou até piorar) em matrizes muito pequenas?
