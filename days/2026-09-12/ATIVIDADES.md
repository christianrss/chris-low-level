# ATIVIDADES — 2026-09-12

**Perfil:** `depth_first` | **1 projeto** | **6–8 h**
**Projeto:** `systems/clvm_xdbg`
**Regra:** não avance sem evidência do checkpoint. Testes PASS sozinhos
não demonstram entendimento.

---

## M1 — Baseline e previsão (30 min)

- [ ] Ler `START_HERE.md` e o README do projeto
- [ ] Executar o starter e registrar as falhas previstas:

```powershell
python scripts/run_day_tests.py --day 2026-09-12 --mode starter --expect-fail
```

## M2 — Modelo mental e testes (60–75 min)

- [ ] Paper-trace de `add2.asm`: header 16 B, PCs, data stack e call stack
- [ ] Relacionar cada trust boundary (tamanho, opcode, bounds, RET) a um caso de `TESTES_GUIADOS.md`

## M3 — Hex e disasm (90 min)

- [ ] `load` + `hex` (header vs code) + `disasm` (PUSH 3, CALL +2)

## M4 — Caminho mínimo end-to-end (2 h)

- [ ] `step` até PRINT/HALT com `prints=[8]`
- [ ] `regs` mostra `call=[13]` imediatamente após o CALL

## M5 — Robustez (60–90 min)

- [ ] Truncamento, 0xFF, underflow, `memory out of bounds`, RET nua
- [ ] Mutantes críticos rejeitados

## M6 — Continue, breakpoints e medição (45–60 min)

- [ ] `break 13` para antes do PRINT
- [ ] Benchmark de N steps com hipótese, mediana e p95
- [ ] Preencher `RUBRIC.md`
