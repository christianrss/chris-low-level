# Resolução guiada — Canal de decoerência (Python)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `Q-DECO-CHANNEL-01` | `starter/decoherence.py` | `depolarizing_channel` |
| `Q-DECO-APPLY-02` | `starter/decoherence.py` | `apply_noise_step` |
| `Q-DECO-TRACE-03` | `starter/decoherence.py` | `trace_decoherence` |

> Raiz: `days/2026-09-09/quantum/decoherence_noise/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/quantum/decoherence_noise/starter
python -m pytest -q 2>$null; if (-not $?) { python test_decoherence.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## Q-DECO-CHANNEL-01

### Onde colocar (Q-DECO-CHANNEL-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/decoherence.py` |
| Função / âncora | `depolarizing_channel` — comentário `TODO [Q-DECO-CHANNEL-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `Q-DECO-CHANNEL-01`, o Caso correspondente falha: p0+p1≈1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `Q-DECO-CHANNEL-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:
    # PEDAGOGY-SOLUTION: Q-DECO-CHANNEL-01
    mix = gamma / 2
    return (1 - gamma) * p0 + mix, (1 - gamma) * p1 + mix
```

### Por que funciona?

Por quê este corpo satisfaz `Q-DECO-CHANNEL-01`: ele implementa exatamente o contrato do
teste (p0+p1≈1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `Q-DECO-CHANNEL-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## Q-DECO-APPLY-02

### Onde colocar (Q-DECO-APPLY-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/decoherence.py` |
| Função / âncora | `apply_noise_step` — comentário `TODO [Q-DECO-APPLY-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `Q-DECO-APPLY-02`, o Caso correspondente falha: nxt[0]<1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `Q-DECO-APPLY-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def apply_noise_step(probs: list[float], gamma: float) -> list[float]:
    # PEDAGOGY-SOLUTION: Q-DECO-APPLY-02
    if len(probs) != 2:
        raise ValueError("2-level only")
    p0, p1 = depolarizing_channel(probs[0], probs[1], gamma)
    return [p0, p1]
```

### Por que funciona?

Por quê este corpo satisfaz `Q-DECO-APPLY-02`: ele implementa exatamente o contrato do
teste (nxt[0]<1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `Q-DECO-APPLY-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## Q-DECO-TRACE-03

### Onde colocar (Q-DECO-TRACE-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/decoherence.py` |
| Função / âncora | `trace_decoherence` — comentário `TODO [Q-DECO-TRACE-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `Q-DECO-TRACE-03`, o Caso correspondente falha: len(tr)==4.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `Q-DECO-TRACE-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:
    # PEDAGOGY-SOLUTION: Q-DECO-TRACE-03
    cur = [p0, 1.0 - p0]
    trace = [cur[0]]
    for _ in range(steps):
        cur = apply_noise_step(cur, gamma)
        trace.append(cur[0])
    return trace
```

### Por que funciona?

Por quê este corpo satisfaz `Q-DECO-TRACE-03`: ele implementa exatamente o contrato do
teste (len(tr)==4.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `Q-DECO-TRACE-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 apply`):
