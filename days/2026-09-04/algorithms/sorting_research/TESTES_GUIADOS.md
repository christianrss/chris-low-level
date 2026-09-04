# Testes guiados — Pesquisa empírica: merge sort vs quicksort

## Objetivo
Os testes precisam verificar invariantes, não apenas "o programa abriu".

## Como executar a solução
```bash
cmake -S projects/chris-algorithms -B build/chris-algorithms -DCMAKE_BUILD_TYPE=Release
cmake --build build/chris-algorithms --config Release
ctest --test-dir build/chris-algorithms --output-on-failure
```

## Casos mínimos
- caminho nominal;
- menor entrada válida;
- edge case relevante;
- input inválido/truncado quando aplicável;
- regressão determinística para o principal invariante.

## Debugging
Se falhar, reduza para o menor caso, imprima/inspecione estado intermediário e confirme primeiro se o seu modelo mental de índice/offset/estado está correto.
