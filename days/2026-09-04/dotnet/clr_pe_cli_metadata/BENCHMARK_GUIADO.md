# Benchmark guiado
Este milestone privilegia correção, não throughput. Como extensão, gere fixtures de 1, 10 e 100 sections e meça apenas `Inspect()` em Release após warmup. A hipótese é que o custo de `RvaToOffset` cresce linearmente com número de sections porque a busca atual é sequencial. Só otimize depois de demonstrar que isso importa.
