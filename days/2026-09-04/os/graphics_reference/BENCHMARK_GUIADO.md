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
