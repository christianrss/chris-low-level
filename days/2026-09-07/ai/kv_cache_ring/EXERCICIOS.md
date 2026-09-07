# Exercícios — KV cache circular

## Fácil — trace no papel (`D5-KV-APPEND`)

**Enunciado:** Com `capacity=4`, simule no papel cinco appends (`p=0..4`). Para cada passo, anote `slot`, conteúdo de `positions[]` e valor de `next_position`.

**Arquivo-alvo:** caderno / `starter/kv_cache.py` (validação opcional com prints).

**Critério de aceite:** identifique qual posição lógica foi evictada no quinto append e em qual slot ela residia antes.

## Médio — append com contiguidade (`D5-KV-APPEND`)

**Enunciado:** Implemente `append` exigindo `position == next_position`. Tente `append(0,...)` seguido de `append(2,...)` e confirme `ValueError`.

**Arquivo-alvo:** `starter/kv_cache.py`.

**Critério de aceite:** quatro appends contíguos em capacity=3 deixam `next_position==4`.

## Difícil — janela e stale read (`D5-KV-WINDOW`)

**Enunciado:** Após wrap em capacity=3, prove que `window(0,1)` falha e `window(1,4)` retorna três pares corretos. Explique o que aconteceria se você checasse só `keys[slot] is not None`.

**Arquivo-alvo:** `starter/kv_cache.py`.

**Critério de aceite:** `KeyError` com mensagem contendo `evicted` para posição 0; ordem k1,k2,k3 na janela válida.

## Desafio — extensão sem quebrar invariante

**Enunciado:** Adicione método `occupied_count()` que retorna quantas posições lógicas ainda são legíveis (`min(next_position, capacity)` antes do wrap completo — documente a fórmula exata). Não altere semântica de `window`.

**Arquivo-alvo:** extensão em `starter/kv_cache.py` + teste local.

**Critério de aceite:** após 4 appends em cap=3, `occupied_count()==3`; após reset, `0`.
