# Benchmark guiado — shader_stage_fsm

## Protocolo

1. Build solutions Release.
2. Rode `test_shader_stage_fsm` 5x; anote tempo wall-clock.
3. Opcional: conte FPS aproximado nas janelas sw/gl (olho + Stopwatch 5s).

## Resultados observados

| Metrica | Valor |
|---------|-------|
| ctest medio (ms) | 15 |
| FPS CPU (approx) | 60 |
| FPS OpenGL (approx) | 60 |
| Notas | FSM trivial; custo e raster/present |

Se nao medir visual: marque FPS como `n/a` e registre so ctest.
