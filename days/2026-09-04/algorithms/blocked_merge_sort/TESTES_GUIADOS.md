# Testes guiados — blocked_merge_sort

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; teste falha enquanto os TODOs permanecem.

## Mapa TODO → teste

### `D2-BLOCK-SORT-TILE`
- Arquivo: `starter/src/blocked_sort.cpp`
- Validação: Caso 2 — vetor que cabe em um tile fica ordenado com `block_reads == block_writes == 1`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-BLOCK-SORT-TILE`

### `D2-BLOCK-MERGE-RUN`
- Arquivo: `starter/src/blocked_sort.cpp`
- Validação: Caso 3/4 — após passes, o vetor multi-tile fica totalmente ordenado.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-BLOCK-MERGE-RUN`

### `D2-BLOCK-PASSES`
- Arquivo: `starter/src/blocked_sort.cpp`
- Validação: Caso 3 — várias distribuições com `tile_size` variado; Caso 1 early-return.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-BLOCK-PASSES`

### `D2-BLOCK-IO-STATS`
- Arquivo: `starter/src/blocked_sort.cpp`
- Validação: Caso 4 — `n=8`, `tile=4` ⇒ `block_reads == 4` e `block_writes == 4`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-BLOCK-IO-STATS`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-algorithms tests passed` e `100% tests passed`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio (ex.: `n` não múltiplo de `tile_size`) e anote qual regressão ele detectaria.
