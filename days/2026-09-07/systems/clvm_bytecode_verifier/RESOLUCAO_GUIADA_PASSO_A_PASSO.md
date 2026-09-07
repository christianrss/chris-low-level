# Resolução guiada — verifier CLVM (N2)

## Baseline

Antes dos TODOs, `starter/verify_clvm.py` valida header v1 (magic, version, flags, entry, code_size, checksum FNV) e inicia decode linear de opcodes. Para cada branch lê `rel` e calcula `target`, mas **não** valida bounds — levanta `NotImplementedError` em `CLVM-VFY-BRANCH-01`. O stack walk inteiro (`CLVM-VFY-STACK-01`) também está ausente.

Estado esperado do starter:

```powershell
cd starter
python verify_clvm.py tests/fixtures/ok.clvm
# INVALID: TODO [CLVM-VFY-BRANCH-01]: check branch target bounds
```

Após ambos os TODOs: `ok.clvm` → VALID; `integration_test.py` → PASS.

Não altere a tabela `STACK_EFFECT`, `BRANCH`, nem a lógica FNV/header já pronta.

---

## Mapa exato starter → resolução

| ID | Arquivo | Função / âncora | Substituir |
|----|---------|-----------------|------------|
| `CLVM-VFY-BRANCH-01` | `starter/verify_clvm.py` | loop linear, após `target = pc + 2 + rel` | `raise NotImplementedError(...BRANCH-01...)` |
| `CLVM-VFY-STACK-01` | idem | final de `verify`, após passagem 1 | `raise NotImplementedError(...STACK-01...)` |

---

## CLVM-VFY-BRANCH-01

### 1. O problema (BRANCH-01)

A passagem 1 já lê `rel` e calcula `target`, mas o starter levanta `NotImplementedError` antes de validar bounds. Saltos OOB passariam silenciosamente até a VM real falhar em PC inválido.

### Onde colocar (BRANCH-01)

| | |
|--|--|
| **Arquivo** | `starter/verify_clvm.py` |
| **Função** | `verify` |
| **Âncora** | bloco `elif op in BRANCH:` — logo após `target = pc + 2 + rel` e `pc += 2` |
| **Substituir** | `raise NotImplementedError("TODO [CLVM-VFY-BRANCH-01]...")` e linhas `_ = (rel, target, start)` |
| **Não mexer** | cálculo de `rel`, FNV, header checks |

### Escreva o código (BRANCH-01)

Remova o `raise` e o `_ = (...)`. Substitua o ramo `elif op in BRANCH:` por:

```python
        elif op in BRANCH:
            if pc + 2 > len(code):
                errors.append(f"truncated branch at {start}")
                break
            rel = struct.unpack_from("<h", code, pc)[0]
            target = pc + 2 + rel
            pc += 2
            if not (0 <= target <= len(code)):
                errors.append(f"branch target OOB from {start} -> {target}")
            else:
                boundaries.add(target)
        boundaries.add(pc)
```

Se o starter não declara `boundaries = {0}` antes do loop linear, adicione essa linha.

### Por que funciona (BRANCH-01)

Saltos relativos i16 definem `target = next_pc + rel`. Limite superior inclusivo (`<= len(code)`) permite alvo no byte após o último opcode — PC válido de parada.

### Verifique (BRANCH-01)

1. `python verify_clvm.py tests/fixtures/ok.clvm` — ainda falha em STACK-01.
2. JMP rel grande negativo → `branch target OOB from 0 -> ...`.
3. `ok.clvm` não emite OOB na passagem 1.

### Debug (BRANCH-01)

Imprima `(start, rel, target, len(code))` antes do `if not`. OOB falso positivo: confira `<` vs `<= len(code)`.

---

## CLVM-VFY-STACK-01

### 1. O problema (STACK-01)

Decode linear valida operandos e saltos, mas não profundidade de pilha. ADD sem dois PUSH prévios passaria na passagem 1 e só falharia na VM — o stack walk fecha essa lacuna.

### Onde colocar (STACK-01)

| | |
|--|--|
| **Arquivo** | `starter/verify_clvm.py` |
| **Função** | `verify` |
| **Âncora** | substituir `# TODO [CLVM-VFY-STACK-01]...` e `raise NotImplementedError(...STACK-01...)` |
| **Substituir** | todo o bloco TODO até `return errors` |
| **Não mexer** | passagem 1 (decode linear), `STACK_EFFECT`, `BRANCH` |

### Escreva o código (STACK-01)

```python
    # conservative stack walk from entry along fall-through only
    # (branches recorded but not fully CFG-merged — flag negative depth)
    depth = 0
    pc = entry
    seen: set[int] = set()
    steps = 0
    while pc < len(code) and steps < 100000:
        if pc in seen:
            break
        seen.add(pc)
        steps += 1
        op = code[pc]
        if op not in STACK_EFFECT:
            break
        pops, pushes = STACK_EFFECT[op]
        if depth < pops:
            errors.append(f"stack underflow at pc={pc} op=0x{op:02x} depth={depth}")
            break
        depth = depth - pops + pushes
        if depth > 1024:
            errors.append(f"stack overflow depth={depth} at pc={pc}")
            break
        pc += 1
        if op == 0x01:
            pc += 4
        elif op in BRANCH:
            rel = struct.unpack_from("<h", code, pc)[0]
            next_pc = pc + 2
            target = next_pc + rel
            if op == 0x09:  # JMP — follow
                pc = target
                continue
            if op == 0x0B:  # CALL — follow target; ignore return path in this pass
                pc = target
                continue
            # JZ/JNZ: follow fall-through (conservative)
            pc = next_pc
            continue
        if op == 0x08:  # HALT
            break
        if op == 0x0C:  # RET — stop this path
            break
    return errors
```

Remova qualquer `return errors  # type: ignore` duplicado abaixo do bloco antigo.

### Por que funciona (STACK-01)

Simula profundidade sem valores reais. JMP/CALL saltam; JZ/JNZ assumem fall-through; `seen` evita loop infinito.

### Verifique (STACK-01)

```powershell
cd starter
python verify_clvm.py tests/fixtures/ok.clvm
python tests/integration_test.py
```

**Esperado:** `VALID` em ok.clvm; `integration_test.py` PASS.

### Debug (STACK-01)

Trace `(pc, op, depth)`. Underflow em ok.clvm: PUSH deve avançar `pc += 4` após `pc += 1`.

---

## Relatório de resolução

Preencha após concluir os dois TODOs:

- **TODOs concluídos:** `CLVM-VFY-BRANCH-01`, `CLVM-VFY-STACK-01`
- **Testes:** starter `integration_test.py` → PASS; `ok.clvm` VALID; `bad_checksum.clvm` INVALID
- **Depuração usada:** (ex.: trace de target OOB, print depth no stack walk)
- **Limites anotados:** walk não faz merge de caminhos JZ taken; CALL não simula retorno
- **Dúvidas:** ___

### Checklist final

- [ ] `0 <= target <= len(code)` na passagem 1
- [ ] Stack walk parte de `entry`, não de 0
- [ ] Mensagens stderr começam com `INVALID:`
- [ ] Não alterou Dia 01 nem FNV
- [ ] Melhorias opcionais documentadas para port em `projects/chris-vm/tools/verify_clvm.py`

Fim da resolução guiada do verifier (N2). Próximo: N3 operador `%%`, depois N4 v2 strings.
