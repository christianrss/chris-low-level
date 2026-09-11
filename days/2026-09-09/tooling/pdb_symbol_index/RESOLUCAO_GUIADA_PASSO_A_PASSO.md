# Resolução guiada — Índice de símbolos estilo PDB (Python)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `TL-PDB-PARSE-01` | `starter/pdb_index.py` | `parse_symbol_line` |
| `TL-PDB-INDEX-02` | `starter/pdb_index.py` | `build_index` |
| `TL-PDB-LOOKUP-03` | `starter/pdb_index.py` | `lookup_symbol` |

> Raiz: `days/2026-09-09/tooling/pdb_symbol_index/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/tooling/pdb_symbol_index/starter
python -m pytest -q 2>$null; if (-not $?) { python test_pdb_index.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## TL-PDB-PARSE-01

### Onde colocar (TL-PDB-PARSE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pdb_index.py` |
| Função / âncora | `parse_symbol_line` — comentário `TODO [TL-PDB-PARSE-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `TL-PDB-PARSE-01`, o Caso correspondente falha: (0x1000,'main').

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `TL-PDB-PARSE-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def parse_symbol_line(line: str) -> tuple[int, str]:
    # PEDAGOGY-SOLUTION: TL-PDB-PARSE-01
    addr_s, name = line.strip().split(None, 1)
    return int(addr_s, 16), name
```

### Por que funciona?

Por quê este corpo satisfaz `TL-PDB-PARSE-01`: ele implementa exatamente o contrato do
teste ((0x1000,'main').), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `TL-PDB-PARSE-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## TL-PDB-INDEX-02

### Onde colocar (TL-PDB-INDEX-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pdb_index.py` |
| Função / âncora | `build_index` — comentário `TODO [TL-PDB-INDEX-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `TL-PDB-INDEX-02`, o Caso correspondente falha: len(idx)==2.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `TL-PDB-INDEX-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def build_index(lines: list[str]) -> dict[int, str]:
    # PEDAGOGY-SOLUTION: TL-PDB-INDEX-02
    idx: dict[int, str] = {}
    for ln in lines:
        if not ln.strip():
            continue
        addr, name = parse_symbol_line(ln)
        idx[addr] = name
    return idx
```

### Por que funciona?

Por quê este corpo satisfaz `TL-PDB-INDEX-02`: ele implementa exatamente o contrato do
teste (len(idx)==2.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `TL-PDB-INDEX-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## TL-PDB-LOOKUP-03

### Onde colocar (TL-PDB-LOOKUP-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pdb_index.py` |
| Função / âncora | `lookup_symbol` — comentário `TODO [TL-PDB-LOOKUP-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `TL-PDB-LOOKUP-03`, o Caso correspondente falha: lookup main.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `TL-PDB-LOOKUP-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def lookup_symbol(idx: dict[int, str], addr: int) -> str:
    # PEDAGOGY-SOLUTION: TL-PDB-LOOKUP-03
    return idx.get(addr, f"0x{addr:x}")
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `TL-PDB-LOOKUP-03`: ele implementa exatamente o contrato do
teste (lookup main.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `TL-PDB-LOOKUP-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 lookup`):
