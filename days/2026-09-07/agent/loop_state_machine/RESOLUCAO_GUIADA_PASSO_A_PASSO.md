# RESOLUÇÃO GUIADA — Agent / loop state machine

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-AGENT-TRANSITION` | `starter/agent_fsm.py` | `AgentFSM.transition` |
| `D5-AGENT-VERIFY` | `starter/agent_fsm.py` | `AgentFSM.verification` |
| `D5-AGENT-REPLAY` | `starter/agent_fsm.py` | `replay` |

IDs: `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` em `solutions/agent_fsm.py`, `PEDAGOGY-TEST: ID` em `starter/test_agent_fsm.py`.

## Baseline

```powershell
cd days/2026-09-07/agent/loop_state_machine/starter
python test_agent_fsm.py
```

**Esperado:** FAIL — `transition` retorna `None` / não avança estados; `replay` falha.

---

## D5-AGENT-TRANSITION — tabela + trace

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/agent_fsm.py` |
| **Função / âncora** | `TODO [D5-AGENT-TRANSITION]` em `transition` |
| **Substituir** | `pass` |
| **Não mexer** | `TRANSITIONS`, `verification`, `replay` |

### 1. O problema

`transition` não muda `self.state` — loop de eventos no teste não chega a VERIFY.

### 2. Código completo

```python
 def transition(self, event):
  key = (self.state, event)
  if key not in TRANSITIONS:
      raise ValueError(f"invalid transition {key}")
  old = self.state
  self.state = TRANSITIONS[key]
  self.seq += 1
  self.trace.append((self.seq, old, event, self.state))
  return self.state
```

### 3. Por que funciona?

- Lookup na tabela global — mesma fonte que `replay` usará.
- Tupla `(seq, old, event, new)` é contrato de auditoria; `seq` detecta buracos.

### 4. Verifique

Após implementar, rode até o teste parar em `verification` — transições até VERIFY devem passar.

---

## D5-AGENT-VERIFY — DONE / REVISE / FAILED

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/agent_fsm.py` |
| **Função / âncora** | `TODO [D5-AGENT-VERIFY]` em `verification` |
| **Substituir** | `pass` |
| **Não mexer** | `transition` já implementado |

### 1. O problema

Sem `verification`, FSM fica em VERIFY — teste espera REVISE após falha e DONE após sucesso.

### 2. Código completo

```python
 def verification(self, passed, evidence):
  if self.state != "VERIFY":
      raise ValueError("not verifying")
  self.evidence.append(evidence)
  old = self.state
  self.seq += 1
  if passed:
      new = "DONE"
      event = "verified"
  elif self.retries < self.max_retries:
      self.retries += 1
      new = "REVISE"
      event = "failed_verify"
  else:
      new = "FAILED"
      event = "retry_exhausted"
  self.state = new
  self.trace.append((self.seq, old, event, new))
  return new
```

### 3. Por que funciona?

- Guard `state=="VERIFY"` impede verify fora de contexto.
- `retries` só sobe quando há revisão — alinha com `max_retries=1` do teste.
- Eventos `verified` / `failed_verify` são o que `replay` valida no ramo VERIFY.

### 4. Verifique

Teste executa ciclo com falha → REVISE → segundo ciclo → DONE. Falha restante só em `replay`.

---

## D5-AGENT-REPLAY — validar trace offline

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/agent_fsm.py` |
| **Função / âncora** | `TODO [D5-AGENT-REPLAY]` em `replay` |
| **Substituir** | `return None` |
| **Não mexer** | classe `AgentFSM` |

### 1. O problema

`replay` stub — último assert `replay(a.trace)=="DONE"` falha.

### 2. Código completo

```python
def replay(trace):
 state = "PERCEIVE"
 expected = 1
 for seq, old, event, new in trace:
  if seq != expected or old != state:
      raise ValueError("trace mismatch")
  if old == "VERIFY":
      if event not in ("verified", "failed_verify", "retry_exhausted"):
          raise ValueError("verify event")
      calc = {"verified": "DONE", "failed_verify": "REVISE", "retry_exhausted": "FAILED"}[event]
  else:
      calc = TRANSITIONS.get((old, event))
  if calc != new:
      raise ValueError("transition mismatch")
  state = new
  expected += 1
 return state
```

### 3. Por que funciona?

- `expected` amarra `seq` contínuo — detecta linhas faltando ou fora de ordem.
- Ramo VERIFY separado porque esses eventos não estão em `TRANSITIONS`.
- Retorna estado final para assert no teste.

### 4. Verifique

```powershell
python test_agent_fsm.py
```

**Esperado:** `chris-agent-fsm tests passed`.

---

## Debug / depuração

| Erro | Ação |
|------|------|
| `invalid transition ('PLAN', 'perceived')` | evento do estado errado — imprima `self.state` |
| `not verifying` | chamou `verification` antes de `observed` |
| `trace mismatch` | compare `a.trace` com estados reais |
| `transition mismatch` em VERIFY | evento não bate com `new` |

Trace esperado mental: `PERCEIVE→PLAN→ACT→OBSERVE→VERIFY→REVISE→PLAN→…→DONE`.

---

## Relatório de resolução

| Campo | Sua resposta |
|-------|----------------|
| Data | |
| Estado onde você travou primeiro | |
| Valor final de `retries` no teste | |
| `replay` retornou | |
| Suite | PASS / FAIL |
