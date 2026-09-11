# Resolução guiada — FSM de pipeline state object

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-GFX-PSO-01` | `starter/pipeline_state_object.py` | `can_transition` |
| `CAP-GFX-PSO-02` | `starter/pipeline_state_object.py` | `apply_transition` |
| `CAP-GFX-PSO-03` | `starter/pipeline_state_object.py` | `pipeline_trace` |

> Raiz: `days/2026-09-10/graphics/pipeline_state_object/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/graphics/pipeline_state_object/starter
python -m pytest -q 2>$null; if (-not $?) { python test_pipeline_state_object.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-GFX-PSO-01

### Onde colocar (CAP-GFX-PSO-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pipeline_state_object.py` |
| Função / âncora | `can_transition` — comentário `TODO [CAP-GFX-PSO-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-GFX-PSO-01`, o Caso correspondente falha: UNINITIALIZED→VERTEX_SHADER.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-GFX-PSO-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def can_transition(current: str, target: str) -> bool:
    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-01
    return target in VALID_TRANSITIONS.get(current, set())
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-GFX-PSO-01`: ele implementa exatamente o contrato do
teste (UNINITIALIZED→VERTEX_SHADER.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-GFX-PSO-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-GFX-PSO-02

### Onde colocar (CAP-GFX-PSO-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pipeline_state_object.py` |
| Função / âncora | `apply_transition` — comentário `TODO [CAP-GFX-PSO-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-GFX-PSO-02`, o Caso correspondente falha: READY→RECORDING.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-GFX-PSO-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def apply_transition(current: str, target: str) -> str:
    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-02
    if not can_transition(current, target):
        raise ValueError(f"invalid {current}->{target}")
    return target
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-GFX-PSO-02`: ele implementa exatamente o contrato do
teste (READY→RECORDING.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-GFX-PSO-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-GFX-PSO-03

### Onde colocar (CAP-GFX-PSO-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pipeline_state_object.py` |
| Função / âncora | `pipeline_trace` — comentário `TODO [CAP-GFX-PSO-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-GFX-PSO-03`, o Caso correspondente falha: pipeline_trace ok.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-GFX-PSO-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def pipeline_trace(states: list[str]) -> bool:
    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-03
    if not states or states[0] != "UNINITIALIZED":
        return False
    for a, b in zip(states, states[1:]):
        if not can_transition(a, b):
            return False
    return True
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-GFX-PSO-03`: ele implementa exatamente o contrato do
teste (pipeline_trace ok.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-GFX-PSO-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 transitions`):
