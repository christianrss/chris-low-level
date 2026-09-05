# Benchmark guiado — arena_allocator

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

Registre na sua máquina (Release, mesma seed de alocações):

| Métrica | Referência típica (ordem de grandeza) | Notas |
|---------|---------------------------------------|-------|
| Alocações arena (10k × 32 B) | 3–8× mais rápido que `new/delete` loop | sem destruição por objeto no loop arena |
| Reset arena | < 1 µs | O(1) independente de contagem |
| Overhead alinhamento 32 | +0–31 bytes por alocação | fragmentação interna |

Valores variam com CPU, allocator do sistema e flags `-O2/-O3`. Use mediana de ≥5 runs após warm-up. Se arena não ganhar, verifique se o benchmark mede também destruição heap — comparação injusta.
