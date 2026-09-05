# Benchmark guiado — protocol_v1

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

300k iterações encode+decode, payload 64 bytes:

| Métrica | Faixa típica (Release) |
|---------|------------------------|
| Round-trips/s | 200k–600k |
| µs/packet | 1.7–5.0 |
| Alocações | estável após warm-up |

Payload maior aumenta tempo linearmente; header fixo 20 B domina em payloads muito pequenos. Compare apenas mesma versão do protocolo e mesmo tamanho de payload.
