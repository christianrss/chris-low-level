# Benchmark guiado — CHRLE em Rust

**Pergunta:** como o tempo de `encode`/`decode` escala com runs longos vs dados incompressíveis, e qual o overhead de `Result` vs retorno direto?

## Procedimento

1. `cargo test --release` ou um `main` scratch em `solutions/`.
2. Para N ∈ {1_000, 100_000, 1_000_000}:
   - payload constante (1 run longo);
   - payload alternado (N runs).
3. Cronometre 50–200 iterações; registre mediana.
4. Opcional: compare com o lab C++ `systems/rle_byte_codec` no mesmo hardware.

## Hipóteses

| Payload | Comportamento |
|---------|----------------|
| constante | encode O(N) mas poucos pushes de par |
| alternado | mais pares → mais pressão em `Vec` |
| decode | sempre O(N) expandido |

## Resultados observados

Ambiente: lab `rust/rle_byte_codec/solutions`, `cargo` release quando disponível.

| N | nota |
|--:|------|
| 1e3 | custo fixo domina |
| 1e5 | throughput bound por alocação |
| 1e6 | n/a microbenchmark sem harness dedicado |

**Skip honesto** de ns absolutos sem `criterion` no repo. Conclusão qualitativa: o formato CHRLE é O(N); em Rust o custo dominante é alocar/expandir, não o `match` de `Result`.

**Conclusão:** preferir `with_capacity(len)` no decode; nunca pular checagem de magic por “performance”.
