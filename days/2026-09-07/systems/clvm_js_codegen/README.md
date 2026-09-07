# Ordem de estudo

1. `TEORIA_PASSO_A_PASSO.md`
2. Completar TODOs em `starter/js2clvm/codegen.py`
3. `python tests/integration_test.py` no starter (esperado FAIL) e em solutions (PASS)
4. Portar insights para `projects/chris-vm/tools/js2clvm`

---

# CLVM JS codegen — Dia 2026-09-07 (N1)

Você **implementa o lowering** JS subset → asm CLVM. Lexer/parser já vêm prontos. A VM continua a do Dia 04 / chris-vm (v1).

## Pré-requisitos

- Dia 01 `systems/clvm` + Dia 04 `clvm_extended`
- Capstone: checklist N0 em `projects/chris-vm/docs/STUDY_CHECKLIST_N0.md`
- Python 3.10+

## TODOs

| ID | O quê |
|----|--------|
| `CLVM-JS-LET-01` | `let`/`const` → expr + STORE |
| `CLVM-JS-WHILE-01` | `while` → labels + JZ/JMP |
| `CLVM-JS-CALL-01` | args + CALL + prólogo STORE dos params |

## Teste

```powershell
cd days/2026-09-07/systems/clvm_js_codegen/solutions
python tests/integration_test.py
```

## Portar

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-vm` |
| O quê | codegen alinhado / melhorias |
| Commit | `feat(vm): js codegen lab day07` |
