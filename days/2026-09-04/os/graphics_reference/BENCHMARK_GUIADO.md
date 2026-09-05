# Benchmark guiado — graphics_reference

## Protocolo mínimo
- escreva hipótese antes de medir;
- build Release quando possível;
- warm-up antes das medições comparativas;
- pelo menos 5 repetições para comparação séria;
- registre CPU, SO, compilador, flags e input;
- guarde resultado bruto e mediana;
- não misture alteração de algoritmo com alteração de flags/hardware na mesma comparação.

O benchmark executável está em `starter/benchmarks/` e é habilitado por `-DCHRIS_BUILD_BENCHMARKS=ON`. A interpretação específica está em `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`.

## Resultados observados

640×360, 40 frames, 2 layers semi-transparentes (Release):

| Métrica | Faixa típica | Notas |
|---------|-------------|-------|
| FPS compositor CPU | 25–120 | depende de cores e compiler |
| ms/frame | 8–40 | inverso do FPS |
| pixels/frame | 230 400 | 640×360 |

Primeira execução pode ser mais lenta (cache frio). Use mediana de 40 frames após warm-up de 5. Baseline antes de SIMD/damage rects no chris-os.
