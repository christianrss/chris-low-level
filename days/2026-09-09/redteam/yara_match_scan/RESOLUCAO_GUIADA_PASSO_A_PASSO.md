# Resolução guiada — Scan estilo YARA (Python)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `RT-YARA-PARSE-01` | `starter/yara_scan.py` | `parse_hex_pattern` |
| `RT-YARA-MATCH-02` | `starter/yara_scan.py` | `match_at` |
| `RT-YARA-TRIAGE-03` | `starter/yara_scan.py` | `scan_all` |

> Raiz: `days/2026-09-09/redteam/yara_match_scan/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/redteam/yara_match_scan/starter
python -m pytest -q 2>$null; if (-not $?) { python test_yara_scan.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## RT-YARA-PARSE-01

### Onde colocar (RT-YARA-PARSE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/yara_scan.py` |
| Função / âncora | `parse_hex_pattern` — comentário `TODO [RT-YARA-PARSE-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `RT-YARA-PARSE-01`, o Caso correspondente falha: pat == [0xAA, None].

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `RT-YARA-PARSE-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def parse_hex_pattern(pat: str) -> list[int | None]:
    # PEDAGOGY-SOLUTION: RT-YARA-PARSE-01
    body = pat.strip("{} ").replace(" ", "")
    out: list[int | None] = []
    i = 0
    while i < len(body):
        if body[i:i+2] == "??":
            out.append(None); i += 2
        else:
            out.append(int(body[i:i+2], 16)); i += 2
    return out
```

### Por que funciona?

Por quê este corpo satisfaz `RT-YARA-PARSE-01`: ele implementa exatamente o contrato do
teste (pat == [0xAA, None].), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `RT-YARA-PARSE-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## RT-YARA-MATCH-02

### Onde colocar (RT-YARA-MATCH-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/yara_scan.py` |
| Função / âncora | `match_at` — comentário `TODO [RT-YARA-MATCH-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `RT-YARA-MATCH-02`, o Caso correspondente falha: match_at offset 1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `RT-YARA-MATCH-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:
    # PEDAGOGY-SOLUTION: RT-YARA-MATCH-02
    if off + len(pattern) > len(data):
        return False
    for i, b in enumerate(pattern):
        if b is not None and data[off + i] != b:
            return False
    return True
```

### Por que funciona?

Por quê este corpo satisfaz `RT-YARA-MATCH-02`: ele implementa exatamente o contrato do
teste (match_at offset 1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `RT-YARA-MATCH-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## RT-YARA-TRIAGE-03

### Onde colocar (RT-YARA-TRIAGE-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/yara_scan.py` |
| Função / âncora | `scan_all` — comentário `TODO [RT-YARA-TRIAGE-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `RT-YARA-TRIAGE-03`, o Caso correspondente falha: scan_all == [1].

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `RT-YARA-TRIAGE-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:
    # PEDAGOGY-SOLUTION: RT-YARA-TRIAGE-03
    return [i for i in range(len(data)) if match_at(data, pattern, i)]
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `RT-YARA-TRIAGE-03`: ele implementa exatamente o contrato do
teste (scan_all == [1].), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `RT-YARA-TRIAGE-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`scan_all em 1MB sintético`):
