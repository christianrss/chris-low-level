# Resolução guiada — Verify + replay log FSM (Python)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `AG-VERIFY-LOG-01` | `starter/agent_log.py` | `append_log` |
| `AG-REPLAY-FSM-02` | `starter/agent_log.py` | `replay_fsm` |
| `AG-TRACE-HASH-03` | `starter/agent_log.py` | `trace_hash` |

> Raiz: `days/2026-09-09/agent/verify_replay_log/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/agent/verify_replay_log/starter
python -m pytest -q 2>$null; if (-not $?) { python test_agent_log.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## AG-VERIFY-LOG-01

### Onde colocar (AG-VERIFY-LOG-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/agent_log.py` |
| Função / âncora | `append_log` — comentário `TODO [AG-VERIFY-LOG-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `AG-VERIFY-LOG-01`, o Caso correspondente falha: len(log)==1 após start.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `AG-VERIFY-LOG-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def append_log(log: list[dict], event: str, payload: dict) -> None:
    # PEDAGOGY-SOLUTION: AG-VERIFY-LOG-01
    log.append({"event": event, "payload": payload})
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `AG-VERIFY-LOG-01`: ele implementa exatamente o contrato do
teste (len(log)==1 após start.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `AG-VERIFY-LOG-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## AG-REPLAY-FSM-02

### Onde colocar (AG-REPLAY-FSM-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/agent_log.py` |
| Função / âncora | `replay_fsm` — comentário `TODO [AG-REPLAY-FSM-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `AG-REPLAY-FSM-02`, o Caso correspondente falha: replay == DONE.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `AG-REPLAY-FSM-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def replay_fsm(log: list[dict]) -> str:
    # PEDAGOGY-SOLUTION: AG-REPLAY-FSM-02
    state = "IDLE"
    for entry in log:
        ev = entry["event"]
        if ev == "start":
            state = "RUN"
        elif ev == "verify" and entry["payload"].get("ok"):
            state = "DONE"
        elif ev == "verify":
            state = "REVISE"
    return state
```

### Por que funciona?

Por quê este corpo satisfaz `AG-REPLAY-FSM-02`: ele implementa exatamente o contrato do
teste (replay == DONE.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `AG-REPLAY-FSM-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## AG-TRACE-HASH-03

### Onde colocar (AG-TRACE-HASH-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/agent_log.py` |
| Função / âncora | `trace_hash` — comentário `TODO [AG-TRACE-HASH-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `AG-TRACE-HASH-03`, o Caso correspondente falha: hash len 16.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `AG-TRACE-HASH-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def trace_hash(log: list[dict]) -> str:
    # PEDAGOGY-SOLUTION: AG-TRACE-HASH-03
    data = repr(log).encode()
    return hashlib.sha256(data).hexdigest()[:16]
```

### Por que funciona?

Por quê este corpo satisfaz `AG-TRACE-HASH-03`: ele implementa exatamente o contrato do
teste (hash len 16.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `AG-TRACE-HASH-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 append+hash`):
