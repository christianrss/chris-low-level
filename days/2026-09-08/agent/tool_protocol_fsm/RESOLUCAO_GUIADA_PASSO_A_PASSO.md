# Resolução guiada — tool_protocol_fsm

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `AGT-TOOL-01` | `starter/tool_protocol_fsm.py` | `transition` | corpo sob `TODO [AGT-TOOL-01]` | assinaturas e testes |
| `AGT-TOOL-02` | `starter/tool_protocol_fsm.py` | `handle_response` | corpo sob `TODO [AGT-TOOL-02]` | assinaturas e testes |
| `AGT-TOOL-03` | `starter/tool_protocol_fsm.py` | `validate_tool_call` | corpo sob `TODO [AGT-TOOL-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/agent/tool_protocol_fsm/starter
python test_tool_protocol_fsm.py
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## AGT-TOOL-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tool_protocol_fsm.py` |
| Função / âncora | `transition` / comentário `TODO [AGT-TOOL-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem transition, IDLE não vai a CALLING.

### Algoritmo / trace

lookup TRANSITIONS; raise se ausente; atualize state/trace.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```python
def transition(self, event: str) -> str:
        # PEDAGOGY-SOLUTION: AGT-TOOL-01
        key = (self.state, event)
        if key not in TRANSITIONS:
            raise ValueError(key)
        self.state = TRANSITIONS[key]
        self.trace.append(f"{event}->{self.state}")
        return self.state
```

### Por que funciona?

A rotina `transition` materializa o contrato de `AGT-TOOL-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `AGT-TOOL-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `AGT-TOOL-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## AGT-TOOL-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tool_protocol_fsm.py` |
| Função / âncora | `handle_response` / comentário `TODO [AGT-TOOL-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem handle_response, WAITING não fecha.

### Algoritmo / trace

transition ok/err; retorne state+keys.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```python
def handle_response(self, ok: bool, payload: dict) -> dict:
        # PEDAGOGY-SOLUTION: AGT-TOOL-02
        self.transition("ok" if ok else "err")
        return {"state": self.state, "payload_keys": list(payload.keys())}
```

### Por que funciona?

A rotina `handle_response` materializa o contrato de `AGT-TOOL-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `AGT-TOOL-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `AGT-TOOL-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## AGT-TOOL-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tool_protocol_fsm.py` |
| Função / âncora | `validate_tool_call` / comentário `TODO [AGT-TOOL-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem validate, nome vazio passa.

### Algoritmo / trace

bool(name) and isinstance(args, dict).

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```python
def validate_tool_call(self, name: str, args: dict) -> bool:
        # PEDAGOGY-SOLUTION: AGT-TOOL-03
        if not name:
            return False
        return isinstance(args, dict)
```

### Por que funciona?

A rotina `validate_tool_call` materializa o contrato de `AGT-TOOL-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `AGT-TOOL-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `AGT-TOOL-03` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| FAIL no Caso 1 | stub intacto / endian errado | releia o trace da TEORIA e o bloco do primeiro TODO |
| PASS parcial | size/estado desalinhado no TODO do meio | imprima pc/head/estado antes do assert |
| Crash / panic | bounds | valide Length/len antes de indexar |
| Diff de string | snprintf/format | compare caractere a caractere com o esperado |

## Relatório de resolução

| TODO | Horas | Maior bug | O que aprendia de novo |
|------|-------|-----------|------------------------|
| `AGT-TOOL-01` |  |  |  |
| `AGT-TOOL-02` |  |  |  |
| `AGT-TOOL-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
