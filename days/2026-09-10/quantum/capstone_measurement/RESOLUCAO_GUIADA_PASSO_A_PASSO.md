# Resolução guiada — Medição Born e amostragem

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-Q-MEAS-01` | `starter/capstone_measurement.py` | `born_probability` |
| `CAP-Q-MEAS-02` | `starter/capstone_measurement.py` | `collapse` |
| `CAP-Q-MEAS-03` | `starter/capstone_measurement.py` | `measure_sample` |

> Raiz: `days/2026-09-10/quantum/capstone_measurement/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/quantum/capstone_measurement/starter
python -m pytest -q 2>$null; if (-not $?) { python test_capstone_measurement.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-Q-MEAS-01

### Onde colocar (CAP-Q-MEAS-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_measurement.py` |
| Função / âncora | `born_probability` — comentário `TODO [CAP-Q-MEAS-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-Q-MEAS-01`, o Caso correspondente falha: Born≈0.5.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-Q-MEAS-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def born_probability(amplitude: complex) -> float:
    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-01
    return abs(amplitude) ** 2
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-Q-MEAS-01`: ele implementa exatamente o contrato do
teste (Born≈0.5.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-Q-MEAS-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-Q-MEAS-02

### Onde colocar (CAP-Q-MEAS-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_measurement.py` |
| Função / âncora | `collapse` — comentário `TODO [CAP-Q-MEAS-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-Q-MEAS-02`, o Caso correspondente falha: c[1]==1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-Q-MEAS-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def collapse(state: list[complex], index: int) -> list[complex]:
    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-02
    n = len(state)
    out = [0j] * n
    out[index] = 1 + 0j
    return out
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-Q-MEAS-02`: ele implementa exatamente o contrato do
teste (c[1]==1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-Q-MEAS-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-Q-MEAS-03

### Onde colocar (CAP-Q-MEAS-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_measurement.py` |
| Função / âncora | `measure_sample` — comentário `TODO [CAP-Q-MEAS-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-Q-MEAS-03`, o Caso correspondente falha: sample→1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-Q-MEAS-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def measure_sample(probs: list[float], u: float) -> int:
    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-03
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if u < acc:
            return i
    return len(probs) - 1 if probs else 0
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-Q-MEAS-03`: ele implementa exatamente o contrato do
teste (sample→1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-Q-MEAS-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 born+sample`):
