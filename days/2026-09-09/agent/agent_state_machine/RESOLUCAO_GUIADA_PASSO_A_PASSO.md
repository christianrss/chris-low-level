# Resolucao guiada — agent_state_machine

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-AGENT-TRANSITIONS` | `starter/agent_state_machine.py` | `next_state` |
| `D7-AGENT-RUN` | `starter/agent_state_machine.py` | `run` |
| `D7-AGENT-TRACE` | `starter/agent_state_machine.py` | `run` |


## Baseline

```powershell
cd days/2026-09-09/agent/agent_state_machine/starter
python test_agent_state_machine.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-AGENT-TRANSITIONS

### Onde colocar (D7-AGENT-TRANSITIONS)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/agent_state_machine.py` |
| Funcao | `next_state` |
| Substituir | corpo sob `TODO [D7-AGENT-TRANSITIONS]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-AGENT-TRANSITIONS` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    m={("PERCEIVE","perceived"):"PLAN",("PLAN","planned"):"ACT",("ACT","acted"):"OBSERVE",("OBSERVE","observed"):"VERIFY",("VERIFY","passed"):"DONE",("VERIFY","failed"):"REVISE",("REVISE","revised"):"ACT",("VERIFY","exhausted"):"FAILED"}
    if (state,event) not in m:raise ValueError("invalid transition")
    return m[(state,event)]
def run(task,tool,verify,max_retries=2):
    state="PERCEIVE";trace=[];retry=0
    def step(event,data):
        nonlocal state
        trace.append({"state":state,"event":event,"data":data});state=next_state(state,event)
```

### Por que funciona?
Materializa o contrato numerico de `D7-AGENT-TRANSITIONS`.

### Verifique
Baseline parcial; `D7-AGENT-TRANSITIONS` PASS.

### Checkpoint
- [ ] `D7-AGENT-TRANSITIONS` PASS

## D7-AGENT-RUN

### Onde colocar (D7-AGENT-RUN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/agent_state_machine.py` |
| Funcao | `run` |
| Substituir | corpo sob `TODO [D7-AGENT-RUN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-AGENT-RUN` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    state="PERCEIVE";trace=[];retry=0
    def step(event,data):
        nonlocal state
        trace.append({"state":state,"event":event,"data":data});state=next_state(state,event)
    step("perceived",{"task":task});step("planned",{"summary":"attempt task"})
    while True:
        result=tool(task,retry);step("acted",{"retry":retry,"ok":result.ok});step("observed",{"evidence":result.evidence})
        if verify(result):step("passed",{"verified":True});return state,trace
```

### Por que funciona?
Materializa o contrato numerico de `D7-AGENT-RUN`.

### Verifique
Baseline parcial; `D7-AGENT-RUN` PASS.

### Checkpoint
- [ ] `D7-AGENT-RUN` PASS

## D7-AGENT-TRACE

### Onde colocar (D7-AGENT-TRACE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/agent_state_machine.py` |
| Funcao | `run` |
| Substituir | corpo sob `TODO [D7-AGENT-TRACE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-AGENT-TRACE` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    state="PERCEIVE";trace=[];retry=0
    def step(event,data):
        nonlocal state
        trace.append({"state":state,"event":event,"data":data});state=next_state(state,event)
    step("perceived",{"task":task});step("planned",{"summary":"attempt task"})
    while True:
        result=tool(task,retry);step("acted",{"retry":retry,"ok":result.ok});step("observed",{"evidence":result.evidence})
        if verify(result):step("passed",{"verified":True});return state,trace
```

### Por que funciona?
Materializa o contrato numerico de `D7-AGENT-TRACE`.

### Verifique
Baseline parcial; `D7-AGENT-TRACE` PASS.

### Checkpoint
- [ ] `D7-AGENT-TRACE` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco |
| off-by-one | size | refaca trace |

## Relatorio de resolucao

- TODOs:
- Saida:
- Invariantes:
- Benchmark: nao executado
