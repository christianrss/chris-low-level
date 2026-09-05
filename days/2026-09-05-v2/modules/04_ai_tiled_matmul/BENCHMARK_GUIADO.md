# Benchmark guiado

O script `benchmarks/run_benchmarks.py` compila a solution em `-O2`, faz 2 warm-ups e 9 repetições em 128x128. Registra mediana naive e tiled. Sempre confira `check=128` para impedir otimização indevida/resultado errado. Resultado real desta reconstrução: veja `benchmarks/results-2026-09-05.md`.