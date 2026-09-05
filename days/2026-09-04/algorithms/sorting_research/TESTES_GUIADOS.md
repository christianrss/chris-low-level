# Testes guiados — sorting_research

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; merge/quick falham enquanto incompletos.

## Mapa TODO → teste

### `D2-SORT-MERGE-RECURSE`
- Arquivo: `starter/src/sort.cpp`
- Validação: merge sort deve ordenar vazio, unitário, aleatório, ordenado e reverso.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-SORT-MERGE-RECURSE`

### `D2-SORT-MERGE-RANGE`
- Arquivo: `starter/src/sort.cpp`
- Validação: merge deve combinar as metades mantendo a ordem e incrementar stats.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-SORT-MERGE-RANGE`

### `D2-SORT-PARTITION`
- Arquivo: `starter/src/sort.cpp`
- Validação: quicksort deve posicionar o pivot e ordenar casos com duplicatas.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-SORT-PARTITION`

### `D2-SORT-QUICK-LOOP`
- Arquivo: `starter/src/sort.cpp`
- Validação: quicksort completo deve ordenar todos os vetores e registrar comparações.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-SORT-QUICK-LOOP`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-algorithms tests passed`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
