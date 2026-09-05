# Testes guiados

### Caso 1: `test_matmul` valida naive 2×3·3×2 e equivalência tiled.
### Caso 2: **Trace 4×4:** `trace_tile_4x4(5,7,4)` → tile (1,1).
### Caso 3: **64×64:** matrizes 64×64 com tile=8 devem coincidir (tolerância 1e-3).
### Caso 4: **Benchmark unificado:** `bench_matmul` imprime `naive_avg_ms` e `tiled_avg_ms` para N=64.
### Caso 5: Valide solutions/ após implementar ambos os TODOs.

## AI-MM-NAIVE-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: AI-MM-NAIVE-01`.

## AI-MM-TILED-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: AI-MM-TILED-02`.
