# Benchmark guiado — CLVM extended

## Protocolo

1. Build Release de `solutions/`.
2. Monte um loop longo (ex. contar até N com LT/JNZ em mem).
3. Cronometre `clvm` para N ∈ {1e3, 1e5, 1e6}.
4. Compare com o countdown só-JMP/JZ do Dia 01 se tiver o binário.

## Resultados observados

| N | tempo (s) | notes |
|---|-----------|-------|
| 1e3 | N/A | não executado neste ambiente de CI |
| 1e5 | N/A | rode localmente e anote mediana |
| 1e6 | N/A | |

Ambiente: lab `clvm_extended/solutions`.
