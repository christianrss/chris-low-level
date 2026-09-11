# Resolução guiada — Tokenizer + merge de runs

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-AI-TOK-01` | `starter/capstone_tokenizer.py` | `bytes_to_ids` |
| `CAP-AI-TOK-02` | `starter/capstone_tokenizer.py` | `merge_runs` |
| `CAP-AI-TOK-03` | `starter/capstone_tokenizer.py` | `vocab_size` |

> Raiz: `days/2026-09-10/ai/capstone_tokenizer/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/ai/capstone_tokenizer/starter
python -m pytest -q 2>$null; if (-not $?) { python test_capstone_tokenizer.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-AI-TOK-01

### Onde colocar (CAP-AI-TOK-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_tokenizer.py` |
| Função / âncora | `bytes_to_ids` — comentário `TODO [CAP-AI-TOK-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-AI-TOK-01`, o Caso correspondente falha: ids aaab.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-AI-TOK-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def bytes_to_ids(data: bytes) -> list[int]:
    # PEDAGOGY-SOLUTION: CAP-AI-TOK-01
    return list(data)
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-AI-TOK-01`: ele implementa exatamente o contrato do
teste (ids aaab.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-AI-TOK-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-AI-TOK-02

### Onde colocar (CAP-AI-TOK-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_tokenizer.py` |
| Função / âncora | `merge_runs` — comentário `TODO [CAP-AI-TOK-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-AI-TOK-02`, o Caso correspondente falha: merge_runs.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-AI-TOK-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def merge_runs(ids: list[int]) -> list[tuple[int, int]]:
    # PEDAGOGY-SOLUTION: CAP-AI-TOK-02
    if not ids:
        return []
    out = []
    cur, run = ids[0], 1
    for x in ids[1:]:
        if x == cur:
            run += 1
        else:
            out.append((cur, run))
            cur, run = x, 1
    out.append((cur, run))
    return out
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-AI-TOK-02`: ele implementa exatamente o contrato do
teste (merge_runs.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-AI-TOK-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-AI-TOK-03

### Onde colocar (CAP-AI-TOK-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_tokenizer.py` |
| Função / âncora | `vocab_size` — comentário `TODO [CAP-AI-TOK-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-AI-TOK-03`, o Caso correspondente falha: vocab_size==2.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-AI-TOK-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def vocab_size(ids: list[int]) -> int:
    # PEDAGOGY-SOLUTION: CAP-AI-TOK-03
    return len(set(ids))
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-AI-TOK-03`: ele implementa exatamente o contrato do
teste (vocab_size==2.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-AI-TOK-03`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.


## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| NotImplemented / stub | corpo não substituído | cole o bloco do TODO |
| número/string diferente | trace errado no papel | refaça a seção 4 da TEORIA |
| caso seguinte quebra | mudou assinatura ou estado global | restaure o que “Não mexer” pede |
| listener/null (.NET) | sem ActivityListener | veja TESTES_GUIADOS |

## Checkpoint intermediário de integração

Depois do primeiro TODO que compila:

1. Rode o teste do módulo a partir de `starter/` (ou o comando do Baseline).
2. Confirme que o Caso 1 ainda falha **só** nos TODOs restantes (não por link quebrado).
3. Anote a mensagem de assert: ela aponta o próximo ID.

## Passo a passo de edição (operacional)

Para cada TODO restante, repita:

1. Abra o arquivo da tabela **Onde colocar**.
2. Localize o comentário `TODO [ID]` — não busque pelo nome do módulo na pasta pai.
3. Substitua **apenas** o corpo indicado; preserve assinatura e includes.
4. Compile; se o erro for de tipo/assinatura, você editou demais.
5. Só então avance ao próximo ID.

## Tabela de regressão rápida

| Depois de | Deve passar | Ainda pode falhar |
|-----------|-------------|-------------------|
| 1º TODO | asserts só desse ID | IDs seguintes |
| 2º TODO | IDs 1–2 | IDs seguintes |
| último TODO | suite inteira | — |

## Armadilhas específicas deste starter

- Mudar o teste para “passar” invalida o lab.
- Criar um segundo `.c`/`.py` com o mesmo símbolo gera link duplicado ou import errado.
- Reset ausente entre casos deixa estado (anel, FSM, arena) contaminado.

## Relatório — campos extras

Além do template padrão, anote:

- Tempo até o primeiro Caso 1 verde:
- Quantas vezes o endianness/size foi a causa:
- Um invariante que você quase violou:

## Relatório de resolução

- TODOs concluídos:
- Comando de teste:
- Saída observada:
- Invariantes checadas:
- Edge cases:
- Benchmark (`1e5 merge_runs`):
