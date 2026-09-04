# Benchmark guiado - P2P: gossip e deduplicacao

1. Defina o que esta sendo medido; nao misture startup, I/O e algoritmo sem perceber.
2. Use Release/otimizacao quando aplicavel.
3. Execute warm-up quando runtime/cache puderem alterar primeiras iteracoes.
4. Repita; preserve mediana e variacao quando fizer sentido.
5. Registre CPU, OS, compilador/runtime, flags e tamanho da entrada.
6. Compare uma mudanca por vez.
7. O benchmark de referencia esta em `projects/chris-p2p/benchmarks/` quando existe.
