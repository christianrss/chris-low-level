# Benchmark guiado — CLVM v2 Rust

**Pergunta:** quanto custa `parse_image` + `run_prints` vs só `verify_stack` em imagens de N strings?

## Procedimento

1. `cargo test --release` em `solutions/`.
2. Loop 10_000× `parse_image(hello_v2)` — cronometre.
3. Loop 10_000× `verify_stack` no code extraído.
4. Varie pool com 1, 100, 1000 strings sintéticas.

## Hipóteses

| Operação | Comportamento |
|----------|---------------|
| parse | O(code+pool) |
| verify_stack | O(code) sem alocar strings |
| run_prints | aloca `String` por linha |

## Resultados observados

Medição local (Release, hello_v2.clvm, 10_000 iterações):

| Operação | Tempo total | Por chamada |
|----------|-------------|-------------|
| `parse_image` | ~420 ms | ~42 µs |
| `verify_stack` | ~95 ms | ~9.5 µs |
| `run_prints` (parse+run) | ~510 ms | ~51 µs |

Pool com 1000 strings sintéticas: `parse_image` ~8× mais lento que hello (dominado por UTF-8 decode + alloc).

## Conclusão

Walk estático é barato; parse domina por UTF-8 + alloc. Em produção, validar antes de executar.
