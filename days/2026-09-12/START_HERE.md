# START HERE — Day 2026-09-12

**Perfil:** depth-first | **Projeto:** `systems/clvm_xdbg` | **Carga:** 6–8 h
**Lane:** systems | **Ciclo:** `depth-core-01`

Você constrói um mini xdbg da CLVM. O Dia 04 já definiu CALL/RET e
memória; hoje o trabalho é **ver** bytes, a instrução em PC, um opcode
por vez, as duas pilhas e a RAM. Não anexe processos Windows.

| Bloco | O que fazer | Evidência |
|-------|-------------|-----------|
| Contrato | Ler `day.contract.yaml` + `ASSESSMENT.yaml` | 6 marcos, 10 comportamentos |
| Baseline | Rodar o starter com `--expect-fail` | `load` ainda não implementado |
| Modelo | Paper-trace de `add2.asm` | hex + PC 0/5/10/13/15 + call=[13] |
| Núcleo | `starter/src/session.cpp` | hex, disasm, step, regs, mem |
| Robustez | Casos 11–15 | underflow, OOB, opcode 0xFF |
| Integração | `break 13` + `continue` | para no PRINT com prints=[] |
| Medição | `python benchmarks/benchmark.py` | median/p95 em results.json |

## Fluxo

1. Teoria do módulo (`CONCEPT-IMAGE-01` … `CONCEPT-BREAK-01`).
2. Previsão das falhas **antes** de abrir a resolução.
3. Implemente só `student_owned` (`starter/src/**`). Host e assembler
   já estão prontos.
4. E2e: sete/oito `step` em add2 → `prints=[8]`.
5. Mutantes `MUTANT-NO-BOUNDS` e `MUTANT-OPSIZE`.
6. Rubrica 75/90 em `RUBRIC.md`.

## Gates

```powershell
python scripts/day_contract_check.py --day 2026-09-12
python scripts/pedagogy_check_unified.py --day 2026-09-12
python scripts/run_day_tests.py --day 2026-09-12 --mode starter --expect-fail
python scripts/run_day_tests.py --day 2026-09-12 --mode solutions
python scripts/run_depth_mutants.py --day 2026-09-12
python scripts/cycle_contract_check.py --cycle depth-core-01
```

Markdown é a fonte primária; DOCX é export opcional.
