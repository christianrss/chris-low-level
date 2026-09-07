# Teoria passo a passo — Agent loop FSM (D5-AGENT)

## 1. O que estamos construindo

Uma **máquina de estados explícita** para harness de coding-agent: `PERCEIVE → PLAN → ACT → OBSERVE → VERIFY`, com ramos `DONE`, `REVISE → PLAN` e `FAILED` após esgotar retries. Cada transição grava `(seq, old_state, event, new_state)`; `replay(trace)` valida determinismo do **controle** sem reexecutar tools.

TODOs: `D5-AGENT-TRANSITION`, `D5-AGENT-VERIFY`, `D5-AGENT-REPLAY`.

## 2. Por que FSM em vez de `while True` opaco

Loops ad-hoc com flags (`planning=False`, `done=None`) escondem invariantes. Em produção (Cursor, CI bots, eval harnesses), você precisa **auditar** o que o agente fez: qual estado, qual evento, qual evidência. FSM + trace permite replay de decisões operacionais, diff entre runs e limites de retry observáveis — sem expor raciocínio interno do modelo.

## 3. Tabela de transições (`D5-AGENT-TRANSITION`)

### O quê

`TRANSITIONS: dict[(state, event)] → next_state` para o pipeline principal:

| Estado atual | Evento | Próximo |
|--------------|--------|---------|
| PERCEIVE | perceived | PLAN |
| PLAN | planned | ACT |
| ACT | acted | OBSERVE |
| OBSERVE | observed | VERIFY |
| REVISE | revised | PLAN |

### Como

`transition(event)`:
1. `key = (self.state, event)`
2. Se `key` ausente → `ValueError`
3. `old = self.state`; `self.state = TRANSITIONS[key]`
4. `self.seq += 1`; append `(seq, old, event, new)` em `self.trace`
5. Retorna `self.state`

### Por quê

Centralizar transições numa tabela evita `if/elif` espalhado e torna **ilegal** combinações não documentadas (ex.: `PLAN` + `acted`). O trace com `seq` monotônico detecta adulteração e gaps em replay.

### Diagrama — pipeline feliz

```text
PERCEIVE --perceived--> PLAN --planned--> ACT --acted--> OBSERVE --observed--> VERIFY
```

### Invariantes

- `transition` só avança estados da tabela — não trata verify/fail (isso é `verification`).
- `seq` estritamente crescente, um incremento por chamada que muta trace.

### Bugs comuns

- Mutar `state` sem registrar trace.
- Aceitar evento em estado errado silenciosamente.
- Confundir nome do evento (`perceived` vs `perceive`).

## 4. Verificação e retries (`D5-AGENT-VERIFY`)

### O quê

`verification(passed, evidence)` só em estado `VERIFY`. Grava evidência estruturada e decide:

| Condição | Novo estado | Evento no trace |
|----------|-------------|-----------------|
| `passed=True` | DONE | verified |
| `passed=False` e `retries < max_retries` | REVISE | failed_verify (+ incrementa retries) |
| `passed=False` e retries esgotados | FAILED | retry_exhausted |

### Como

```text
exigir state == VERIFY
append evidence
seq += 1
se passed: new=DONE, event=verified
senão se retries < max_retries: retries++, new=REVISE, event=failed_verify
senão: new=FAILED, event=retry_exhausted
state ← new; trace.append(...)
```

### Por quê

Sem `max_retries`, harness oscila `VERIFY ↔ REVISE` indefinidamente — comum em evals ruidosos. `FAILED` é stop condition explícita. Evidência (`{"tests": 5}`, exit code) é dado **verificável**, não chain-of-thought do LLM.

### Trace manual — uma falha, depois sucesso (`max_retries=1`)

```text
... → VERIFY
verification(False, {"tests":0}) → REVISE  (retries=1)
revised → PLAN → ... → VERIFY
verification(True, {"tests":5}) → DONE
```

### Invariantes

- `evidence` append-only em lista `self.evidence`.
- `retries` só incrementa em falha com revisão permitida.
- Chamar `verification` fora de VERIFY → `ValueError`.

### Bugs comuns

- Incrementar retries em sucesso.
- Transicionar sem append no trace.
- Esquecer ramo `FAILED`.

## 5. Replay determinístico (`D5-AGENT-REPLAY`)

### O quê

`replay(trace) → final_state` revalida que cada linha do trace é consistente com as regras — **sem** rodar shell, rede ou modelo.

### Como

```text
state ← PERCEIVE; expected_seq ← 1
para (seq, old, event, new) em trace:
  se seq ≠ expected_seq ou old ≠ state: erro
  se old == VERIFY:
    calc ← mapa evento→estado (verified→DONE, ...)
  senão:
    calc ← TRANSITIONS[(old, event)]
  se calc ≠ new: erro
  state ← new; expected_seq++
return state
```

### Por quê

Replay de controle é pré-requisito para **regressão de harness**: você grava trace de um run bom e garante que mudanças no orchestrator não alteram a máquina de estados. Tool results futuros podem ligar por ID; o núcleo é integridade seq/old/event/new.

### Diagrama — replay vs execução real

```text
Run real:  PERCEIVE → tools → PLAN → tools → ...  (efeitos colaterais)
Replay:    trace[] ──► validar só transições ──► estado final
```

### Invariantes

- Primeiro registro deve partir de `PERCEIVE` com `old` coerente.
- Eventos em VERIFY restritos a `verified`, `failed_verify`, `retry_exhausted`.

### Bugs comuns

- Reexecutar `transition()` no replay (duplica lógica e side effects).
- Não validar `seq`.
- Usar `TRANSITIONS` para eventos de verify.

## 6. Evidência vs raciocínio privado

| Gravar no trace/evidence | Não gravar |
|--------------------------|------------|
| exit code, testes passados | chain-of-thought |
| arquivos tocados | “pensamentos” do modelo |
| stderr do compilador | prompts internos |

## 7. Complexidade

| Operação | Tempo |
|----------|-------|
| `transition` | O(1) |
| `verification` | O(1) |
| `replay` | O(len(trace)) |

## 8. Comparação com produção

| Este lab | Harness real |
|----------|--------------|
| 6 estados | dezenas (tool_wait, cancel, human) |
| retry fixo | backoff, política por tipo de erro |
| replay de controle | replay + snapshots de workspace |

## 9. Passo a passo guiado (ordem dos TODOs)

1. `D5-AGENT-TRANSITION` — `transition` + trace.
2. `D5-AGENT-VERIFY` — ramos DONE/REVISE/FAILED.
3. `D5-AGENT-REPLAY` — validação offline.
4. `python starter/test_agent_fsm.py` → `chris-agent-fsm tests passed`.

## 10. Como saber se está correto

- Loop `perceived→planned→acted→observed` deixa FSM em VERIFY.
- `verification(False,...)` com `max_retries=1` → REVISE; após segundo ciclo, `verification(True,...)` → DONE.
- `replay(a.trace) == "DONE"`.

## 11. Bugs comuns (checklist)

| Sintoma | Causa |
|---------|-------|
| `invalid transition` no meio | evento errado para estado |
| replay mismatch em seq | não incrementou ou pulou |
| FAILED nunca ocorre | retries não incrementam |
| VERIFY com `transition` | verify só via `verification()` |

## 12. Por quê este módulo existe

Agentes em produção são **sistemas com estado**. Cada TODO protege propriedade que separa demo de harness confiável: transições legais, limite de retry e replay auditável.
