# Resolução guiada — Driver composto de input

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-LNX-COMP-01` | `starter/composite_input_driver.py` | `register_device` |
| `CAP-LNX-EVDEV-02` | `starter/composite_input_driver.py` | `hid_boot_to_evdev` |
| `CAP-LNX-SYNC-03` | `starter/composite_input_driver.py` | `finalize_frame` |

> Raiz: `days/2026-09-10/linux/composite_input_driver/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/linux/composite_input_driver/starter
python -m pytest -q 2>$null; if (-not $?) { python test_composite_input_driver.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-LNX-COMP-01

### Onde colocar (CAP-LNX-COMP-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/composite_input_driver.py` |
| Função / âncora | `register_device` — comentário `TODO [CAP-LNX-COMP-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-LNX-COMP-01`, o Caso correspondente falha: name composite0.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-LNX-COMP-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def register_device(name: str, capabilities: set[str]) -> dict:
    # PEDAGOGY-SOLUTION: CAP-LNX-COMP-01
    return {"name": name, "capabilities": sorted(capabilities)}
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-LNX-COMP-01`: ele implementa exatamente o contrato do
teste (name composite0.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-LNX-COMP-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-LNX-EVDEV-02

### Onde colocar (CAP-LNX-EVDEV-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/composite_input_driver.py` |
| Função / âncora | `hid_boot_to_evdev` — comentário `TODO [CAP-LNX-EVDEV-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-LNX-EVDEV-02`, o Caso correspondente falha: ev [(1,4,1)].

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-LNX-EVDEV-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def hid_boot_to_evdev(report: bytes) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-LNX-EVDEV-02
    if len(report) != 8:
        return []
    return [(1, b, 1) for b in report[2:8] if b]
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-LNX-EVDEV-02`: ele implementa exatamente o contrato do
teste (ev [(1,4,1)].), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-LNX-EVDEV-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-LNX-SYNC-03

### Onde colocar (CAP-LNX-SYNC-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/composite_input_driver.py` |
| Função / âncora | `finalize_frame` — comentário `TODO [CAP-LNX-SYNC-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-LNX-SYNC-03`, o Caso correspondente falha: frame[-1]==(0,0,0).

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-LNX-SYNC-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def finalize_frame(events: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-LNX-SYNC-03
    return events + [(0, 0, 0)]
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-LNX-SYNC-03`: ele implementa exatamente o contrato do
teste (frame[-1]==(0,0,0).), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-LNX-SYNC-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 frames`):
