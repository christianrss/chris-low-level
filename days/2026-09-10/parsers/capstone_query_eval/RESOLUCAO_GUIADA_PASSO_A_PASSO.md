# Resolução guiada — Query Pratt/bool simples

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-PRATT-01` | `starter/capstone_query_eval.py` | `lex` |
| `CAP-PRATT-02` | `starter/capstone_query_eval.py` | `parse_expr` |
| `CAP-PRATT-03` | `starter/capstone_query_eval.py` | `eval_query` |

> Raiz: `days/2026-09-10/parsers/capstone_query_eval/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/parsers/capstone_query_eval/starter
python -m pytest -q 2>$null; if (-not $?) { python test_capstone_query_eval.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-PRATT-01

### Onde colocar (CAP-PRATT-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_query_eval.py` |
| Função / âncora | `lex` — comentário `TODO [CAP-PRATT-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-PRATT-01`, o Caso correspondente falha: lex 3 tokens.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-PRATT-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def lex(s: str) -> list[str]:
    # PEDAGOGY-SOLUTION: CAP-PRATT-01
    return s.split()
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-PRATT-01`: ele implementa exatamente o contrato do
teste (lex 3 tokens.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-PRATT-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-PRATT-02

### Onde colocar (CAP-PRATT-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_query_eval.py` |
| Função / âncora | `parse_expr` — comentário `TODO [CAP-PRATT-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-PRATT-02`, o Caso correspondente falha: AND True.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-PRATT-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def parse_expr(tokens: list[str], pos: int, min_bp: int) -> tuple[bool, int]:
    # PEDAGOGY-SOLUTION: CAP-PRATT-02
    if pos >= len(tokens):
        return False, pos
    tok = tokens[pos]
    if ":" in tok:
        left = True
        pos += 1
    elif tok == "true":
        left, pos = True, pos + 1
    elif tok == "false":
        left, pos = False, pos + 1
    else:
        return False, pos
    while pos < len(tokens):
        op = tokens[pos]
        if op == "AND" and BP_AND >= min_bp:
            pos += 1
            right, pos = parse_expr(tokens, pos, BP_AND + 1)
            left = left and right
        elif op == "OR" and BP_OR >= min_bp:
            pos += 1
            right, pos = parse_expr(tokens, pos, BP_OR + 1)
            left = left or right
        else:
            break
    return left, pos
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-PRATT-02`: ele implementa exatamente o contrato do
teste (AND True.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-PRATT-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-PRATT-03

### Onde colocar (CAP-PRATT-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_query_eval.py` |
| Função / âncora | `eval_query` — comentário `TODO [CAP-PRATT-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-PRATT-03`, o Caso correspondente falha: OR True.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-PRATT-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def eval_query(s: str) -> bool:
    # PEDAGOGY-SOLUTION: CAP-PRATT-03
    toks = lex(s)
    val, end = parse_expr(toks, 0, 0)
    return val and end == len(toks)
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-PRATT-03`: ele implementa exatamente o contrato do
teste (OR True.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-PRATT-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 eval_query`):
