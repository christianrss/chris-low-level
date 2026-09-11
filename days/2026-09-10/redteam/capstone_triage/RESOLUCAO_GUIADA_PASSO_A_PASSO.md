# Resolução guiada — Triage de magic bytes

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-RT-FMT-01` | `starter/capstone_triage.py` | `detect_magic` |
| `CAP-RT-FMT-02` | `starter/capstone_triage.py` | `min_size_for` |
| `CAP-RT-FMT-03` | `starter/capstone_triage.py` | `triage_report` |

> Raiz: `days/2026-09-10/redteam/capstone_triage/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/redteam/capstone_triage/starter
python -m pytest -q 2>$null; if (-not $?) { python test_capstone_triage.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-RT-FMT-01

### Onde colocar (CAP-RT-FMT-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_triage.py` |
| Função / âncora | `detect_magic` — comentário `TODO [CAP-RT-FMT-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-RT-FMT-01`, o Caso correspondente falha: ELF/PE/WASM detect.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-RT-FMT-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def detect_magic(data: bytes) -> str | None:
    # PEDAGOGY-SOLUTION: CAP-RT-FMT-01
    for name, magic in MAGICS.items():
        if data.startswith(magic):
            return name
    return None
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-RT-FMT-01`: ele implementa exatamente o contrato do
teste (ELF/PE/WASM detect.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-RT-FMT-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-RT-FMT-02

### Onde colocar (CAP-RT-FMT-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_triage.py` |
| Função / âncora | `min_size_for` — comentário `TODO [CAP-RT-FMT-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-RT-FMT-02`, o Caso correspondente falha: min_size PE==2.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-RT-FMT-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def min_size_for(fmt: str) -> int:
    # PEDAGOGY-SOLUTION: CAP-RT-FMT-02
    return {"ELF": 4, "PE": 2, "WASM": 4}.get(fmt, 0)
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-RT-FMT-02`: ele implementa exatamente o contrato do
teste (min_size PE==2.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-RT-FMT-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-RT-FMT-03

### Onde colocar (CAP-RT-FMT-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_triage.py` |
| Função / âncora | `triage_report` — comentário `TODO [CAP-RT-FMT-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-RT-FMT-03`, o Caso correspondente falha: triage ok True.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-RT-FMT-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def triage_report(data: bytes) -> dict:
    # PEDAGOGY-SOLUTION: CAP-RT-FMT-03
    fmt = detect_magic(data)
    if fmt is None:
        return {"format": None, "ok": False, "reason": "unknown magic"}
    need = min_size_for(fmt)
    if len(data) < need:
        return {"format": fmt, "ok": False, "reason": "truncated"}
    return {"format": fmt, "ok": True, "reason": "ok"}
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-RT-FMT-03`: ele implementa exatamente o contrato do
teste (triage ok True.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-RT-FMT-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 detect_magic`):
