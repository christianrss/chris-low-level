# Benchmark guiado
```bash
node --experimental-strip-types starter/benchmarks/bench.ts
```
O benchmark faz warmup e 5 amostras sobre 100.000 linhas. Registre mediana, Node version e tamanho do input. Depois compare `Buffer.concat` com uma estratégia de chunks/offsets para investigar custo de cópia. Não conclua que uma versão é melhor sem considerar memória e complexidade.

## Resultados observados

100k linhas, chunks ~1 KiB (mediana de 5 runs):

| Métrica | Faixa típica |
|---------|-------------|
| linhas/s | 80k–400k |
| ms total | 250–1200 |
| RSS pico | depende de `maxLineBytes` |

Implementação com `Buffer.concat` no remainder é didática, não ótima — cópias extras aparecem em perfil. Backpressure demo não entra neste número; são benchmarks separados.
