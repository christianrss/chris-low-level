# Benchmark guiado — Tiled matmul

## Hipótese

Cache blocking com tile=16 reduz misses de L1 em matmul 128×128, tornando `matmul_tiled` mais rápido que `matmul_naive` em CPU com cache hierárquica.

## Protocolo

1. Compile `solutions/bench_matmul.cpp` com `-O2`.
2. Warm-up: 2 execuções descartáveis.
3. 9 repetições de naive e tiled (128×128, tile=16).
4. Reporte mediana em ms e checksum do resultado.
5. Verifique que checksums coincidem.

## Comando

```bash
cmake -S solutions -B solutions/build -DCMAKE_BUILD_TYPE=Release
cmake --build solutions/build
./solutions/build/bench_matmul
```

## Resultados observados

Ambiente: container Linux, g++ -O2, 2 warm-ups + 9 repetições.

| Métrica | Mediana | Checksum |
|---------|---------|----------|
| `matmul_128_naive_ms` | ~1.84 ms | 128.0 |
| `matmul_128_tiled16_ms` | ~1.09 ms | 128.0 |

**Conclusão:** tiling reduziu ~40% o tempo neste ambiente específico. Em matrizes < 32×32 o overhead de loops extras pode inverter o resultado. Sempre valide checksum — velocidade sem correção é inútil.
