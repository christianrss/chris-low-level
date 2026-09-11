# Resolução guiada — perf_event_open (simulação Python)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `LX-PERF-OPEN-01` | `starter/perf_lab.py` | `perf_event_open` |
| `LX-PERF-READ-02` | `starter/perf_lab.py` | `perf_event_read` |
| `LX-PERF-CLOSE-03` | `starter/perf_lab.py` | `perf_event_close` |

> Raiz: `days/2026-09-09/linux/perf_event_open_lab/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/linux/perf_event_open_lab/starter
python -m pytest -q 2>$null; if (-not $?) { python test_perf_lab.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## LX-PERF-OPEN-01

### Onde colocar (LX-PERF-OPEN-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/perf_lab.py` |
| Função / âncora | `perf_event_open` — comentário `TODO [LX-PERF-OPEN-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `LX-PERF-OPEN-01`, o Caso correspondente falha: fd > 0.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `LX-PERF-OPEN-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def perf_event_open(event_type: int, config: int) -> int:
    # PEDAGOGY-SOLUTION: LX-PERF-OPEN-01
    if event_type < 0:
        return -1
    return (event_type << 16) | (config & 0xFFFF)
```

### Por que funciona?

Por quê este corpo satisfaz `LX-PERF-OPEN-01`: ele implementa exatamente o contrato do
teste (fd > 0.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `LX-PERF-OPEN-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## LX-PERF-READ-02

### Onde colocar (LX-PERF-READ-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/perf_lab.py` |
| Função / âncora | `perf_event_read` — comentário `TODO [LX-PERF-READ-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `LX-PERF-READ-02`, o Caso correspondente falha: read == 42.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `LX-PERF-READ-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def perf_event_read(fd: int, counters: dict[int, int]) -> int:
    # PEDAGOGY-SOLUTION: LX-PERF-READ-02
    return counters.get(fd, 0)
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `LX-PERF-READ-02`: ele implementa exatamente o contrato do
teste (read == 42.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `LX-PERF-READ-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## LX-PERF-CLOSE-03

### Onde colocar (LX-PERF-CLOSE-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/perf_lab.py` |
| Função / âncora | `perf_event_close` — comentário `TODO [LX-PERF-CLOSE-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `LX-PERF-CLOSE-03`, o Caso correspondente falha: close True e fd removido.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `LX-PERF-CLOSE-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def perf_event_close(fd: int, counters: dict[int, int]) -> bool:
    # PEDAGOGY-SOLUTION: LX-PERF-CLOSE-03
    return counters.pop(fd, None) is not None
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `LX-PERF-CLOSE-03`: ele implementa exatamente o contrato do
teste (close True e fd removido.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `LX-PERF-CLOSE-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e6 open/read/close`):
