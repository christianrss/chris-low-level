# Benchmark guiado — N steps da sessão

## Hipótese

Vinte mil fetch/decode/execute da ISA CLVM, num loop `PUSH 1 / DROP /
JMP`, cabem folgados em menos de um segundo neste host. O custo
dominante é o switch do opcode, não I/O.

## Método

1. Compilar `solutions/` (ou o starter já preenchido).
2. `python benchmarks/benchmark.py` — o script acha `clvm-xdbg`, monta
   `spin.asm` e chama `--bench 20000` sete vezes.
3. Métricas: `median`, `p95`, `samples` em nanossegundos.

Não compare com x64dbg: o alvo é regressão da **sua** sessão, não
throughput de um debugger nativo.

## Resultados observados

Execução local após `solutions/` compilado (`--bench 20000`, sete amostras):

| Métrica | Valor |
|---------|------:|
| steps | 20000 |
| median | 119300 ns (~0.12 ms) |
| p95 | 347900 ns (~0.35 ms) |
| samples | 118900, 372400, 119300, 347900, 119100, 119200, 129900 |

A hipótese segura: 20k steps ficam bem abaixo de 1 s. A variação (p95 ~3× a mediana) veio de duas amostras frias; as outras cinco agrupam em ~0.12 ms. Reallocar a data stack a cada `step` provavelmente pioraria o p95 mais do que a mediana.

Números brutos: `benchmarks/results.json`.
