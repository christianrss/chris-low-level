# Benchmark guiado
```bash
node --experimental-strip-types starter/benchmarks/bench.ts
```
O benchmark faz warmup e 5 amostras sobre 100.000 linhas. Registre mediana, Node version e tamanho do input. Depois compare `Buffer.concat` com uma estratégia de chunks/offsets para investigar custo de cópia. Não conclua que uma versão é melhor sem considerar memória e complexidade.
