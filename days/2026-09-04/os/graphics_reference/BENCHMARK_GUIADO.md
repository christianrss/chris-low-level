# Benchmark guiado — graphics_reference

## Protocolo mínimo
- escreva hipótese antes de medir (ex.: damage toca << 230 400 px/frame);
- build Release quando possível;
- warm-up antes das medições comparativas;
- pelo menos 5 repetições para comparação séria;
- registre CPU, SO, compilador, flags e input;
- guarde resultado bruto e mediana;
- não misture alteração de algoritmo com alteração de flags/hardware na mesma comparação.

O benchmark executável está em `starter/benchmarks/` e é habilitado por `-DCHRIS_BUILD_BENCHMARKS=ON`. Interpretação em `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` / apêndice.

## O que o binário imprime

Duas linhas por execução:

- `mode=full` — `Compositor::compose` tela inteira; `pixels_touched = 640×360×frames`
- `mode=damage` — `FramePacer::compose_with_damage` com união dos footprints das janelas; `pixels_touched` = soma de `FrameStats::pixels_touched`

## Resultados observados

640×360, 40 frames, 2 layers semi-transparentes (Release):

| Métrica | Faixa típica | Notas |
|---------|-------------|-------|
| FPS full | 25–120 | depende de cores e compiler |
| FPS damage | ≥ full (CPU-bound) | menos pixels |
| ms/frame full | 8–40 | inverso do FPS |
| pixels/frame full | 230 400 | 640×360 |
| pixels/frame damage | << 230 400 | depende do tamanho da união AABB |

Primeira execução pode ser mais lenta (cache frio). Use mediana após warm-up. Compare **pixels_touched**, não só FPS — pacing/vsync real ainda não está no loop (só o custo de recomposição).
