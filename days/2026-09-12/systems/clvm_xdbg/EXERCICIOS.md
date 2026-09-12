# Exercícios — marcos do mini xdbg

Cada marco bloqueia o seguinte. Testes PASS sozinhos não substituem o
paper-trace. TODOs vivem em `starter/src/session.cpp`.

## M1 — Baseline e previsão (30 min)

Rode o starter e anote que **nenhuma** view funciona ainda (`load`
devolve `not implemented`).

```powershell
python scripts/run_day_tests.py --day 2026-09-12 --mode starter --expect-fail
```

Aceite: a previsão lista truncamento, opcode 0xFF, underflow, OOB e RET
nua como falhas que o núcleo ainda não emite.

## M2 — Modelo mental e paper-trace (60 min)

No papel, para `programs/add2.asm`:

1. hex do header (magic + `code_size=17`)
2. layout de code com PCs 0,5,10,13,14,15,16
3. as duas pilhas após o CALL e após o RET

Aceite: o trace bate com CONCEPT-STEP-01 da teoria. Sem isso, não abra
a resolução.

## M3 — Hex e disasm (90 min)

Implemente `XDBG-LOAD-01`, `XDBG-HEX-01`, `XDBG-DISASM-01`.
`hex` deve marcar header vs code. `disasm` em pc=0 é `PUSH 3`; após
dois `step`, `CALL +2`.

Aceite: casos 1–4 de `TESTES_GUIADOS.md`.

## M4 — Step end-to-end (2 h)

`XDBG-STEP-01` + `XDBG-REGS-01`. Sete `step` em add2 deixam
`prints=[8]` e `status=halted`. Depois do terceiro step, `call=[13]`
e `data=[3,5]`.

Aceite: casos 5, 6 e 10 (e2e).

## M5 — Robustez (75 min)

`XDBG-MEM-01` + `XDBG-ERR-01`. `mem_demo` grava `2A 00 00 00`.
`bad_mem.asm` → `memory out of bounds`. Imagem de 8 bytes →
`file too small`. `0xFF` → `unknown opcode`. PRINT nua →
`stack underflow`. `bad_ret.asm` → `return stack underflow`.

Aceite: casos 7 e 11–15. Mutante NO-BOUNDS rejeitado.

## M6 — Breakpoints, continue e medição (45 min)

`XDBG-BREAK-01`. `break 13` + `continue` para no PRINT com `prints=[]`.
`continue` sem break chega em HALT. Rode o benchmark de 20k steps,
registre mediana/p95, preencha `RUBRIC.md`.

Aceite: casos 8–9 + `benchmarks/results.json`.
