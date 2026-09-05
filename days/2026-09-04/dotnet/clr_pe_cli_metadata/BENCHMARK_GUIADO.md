# Benchmark guiado
Este milestone privilegia correção, não throughput. Como extensão, gere fixtures de 1, 10 e 100 sections e meça apenas `Inspect()` em Release após warmup. A hipótese é que o custo de `RvaToOffset` cresce linearmente com número de sections porque a busca atual é sequencial. Só otimize depois de demonstrar que isso importa.

## Resultados observados

Fixture sintético do teste (2 sections, imagem < 4 KiB):

| Métrica | Faixa típica |
|---------|-------------|
| Inspect() / chamada | 5–30 µs |
| Overhead dominante | leituras bounds-checked + loop de sections |

Com 100 sections simuladas, tempo cresce ~linearmente (~10–50× vs 2 sections) — confirma hipótese de busca sequencial. Não é meta de performance deste dia; documente para justificar índice por RVA no milestone futuro.
