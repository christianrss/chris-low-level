# Resolução guiada — Lexer logfmt (Python)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `PR-LOGFMT-LEX-01` | `starter/logfmt.py` | `tokenize` |
| `PR-LOGFMT-KV-02` | `starter/logfmt.py` | `parse_kv` |
| `PR-LOGFMT-ESC-03` | `starter/logfmt.py` | `parse_line` |

> Raiz: `days/2026-09-09/parsers/logfmt_lexer/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/parsers/logfmt_lexer/starter
python -m pytest -q 2>$null; if (-not $?) { python test_logfmt.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## PR-LOGFMT-LEX-01

### Onde colocar (PR-LOGFMT-LEX-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/logfmt.py` |
| Função / âncora | `tokenize` — comentário `TODO [PR-LOGFMT-LEX-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `PR-LOGFMT-LEX-01`, o Caso correspondente falha: len(tokenize('a=1 b=2'))==2.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `PR-LOGFMT-LEX-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def tokenize(line: str) -> list[str]:
    # PEDAGOGY-SOLUTION: PR-LOGFMT-LEX-01
    return shlex.split(line.strip())
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `PR-LOGFMT-LEX-01`: ele implementa exatamente o contrato do
teste (len(tokenize('a=1 b=2'))==2.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `PR-LOGFMT-LEX-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## PR-LOGFMT-KV-02

### Onde colocar (PR-LOGFMT-KV-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/logfmt.py` |
| Função / âncora | `parse_kv` — comentário `TODO [PR-LOGFMT-KV-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `PR-LOGFMT-KV-02`, o Caso correspondente falha: parse_kv msg=hello.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `PR-LOGFMT-KV-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def parse_kv(tok: str) -> tuple[str, str]:
    # PEDAGOGY-SOLUTION: PR-LOGFMT-KV-02
    k, v = tok.split('=', 1)
    return k, v
```

### Por que funciona?

Por quê este corpo satisfaz `PR-LOGFMT-KV-02`: ele implementa exatamente o contrato do
teste (parse_kv msg=hello.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `PR-LOGFMT-KV-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## PR-LOGFMT-ESC-03

### Onde colocar (PR-LOGFMT-ESC-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/logfmt.py` |
| Função / âncora | `parse_line` — comentário `TODO [PR-LOGFMT-ESC-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `PR-LOGFMT-ESC-03`, o Caso correspondente falha: level==info no dict.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `PR-LOGFMT-ESC-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def parse_line(line: str) -> dict[str, str]:
    # PEDAGOGY-SOLUTION: PR-LOGFMT-ESC-03
    out: dict[str, str] = {}
    for tok in tokenize(line):
        k, v = parse_kv(tok)
        out[k] = v.strip('"')
    return out
```

### Por que funciona?

Por quê este corpo satisfaz `PR-LOGFMT-ESC-03`: ele implementa exatamente o contrato do
teste (level==info no dict.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `PR-LOGFMT-ESC-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 tokenize de linha típica`):
