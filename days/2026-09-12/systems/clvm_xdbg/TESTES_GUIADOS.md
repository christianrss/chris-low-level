# Testes guiados — clvm_xdbg

Todos os casos estão em `starter/tests/test_xdbg.py`. O CTest chama o
binário `clvm-xdbg` com stdin. PRINT da ISA aparece em `regs` como
`prints=[...]`, não no stdout.

## Caso 1: load add2

`test_load_valid_add2` — `ready pc=0`. TODO `XDBG-LOAD-01`.

## Caso 2: hex header e code

`test_hex_header_and_code` — dump contém `43 4C 56 4D`, tags `header` e
`code`, offsets `0000` e `0010`. TODO `XDBG-HEX-01`.

## Caso 3: disasm PUSH 3

`test_disasm_push_at_entry` — `pc=0 PUSH 3`. TODO `XDBG-DISASM-01`.

## Caso 4: disasm CALL +2

`test_disasm_call_operand` — dois `step`, depois `CALL` e `2`.
TODO `XDBG-DISASM-01`.

## Caso 5: step atualiza a data stack

`test_step_push_updates_stack` — após um step, `data=[3]` e `pc=5`.
TODO `XDBG-STEP-01`.

## Caso 6: duas pilhas após CALL

`test_regs_shows_pc_and_stacks` — três steps, `data=[3,5]`, `call=[13]`.
TODO `XDBG-REGS-01`.

## Caso 7: RAM após STORE

`test_mem_view_after_store` — `mem_demo`, três steps, `2A 00 00 00`.
TODO `XDBG-MEM-01`.

## Caso 8: breakpoint no PRINT

`test_breakpoint_stops_before_print` — `break 13`, `continue`,
`status=breakpoint`, `prints=[]`. TODO `XDBG-BREAK-01`.

## Caso 9: continue até HALT

`test_continue_to_halt` — `prints=[8]`, `status=halted`.
TODO `XDBG-BREAK-01`.

## Caso 10: e2e add2

`test_e2e_add2_prints_8` — oito `step`, `prints=[8]`, halted.
TODO `XDBG-STEP-01`.

## Caso 11: truncamento

`test_truncated_image` — 8 bytes, `file too small`. TODO `XDBG-LOAD-01`.

## Caso 12: opcode desconhecido

`test_unknown_opcode` — code `0xFF`, `unknown opcode`. TODO `XDBG-ERR-01`.

## Caso 13: stack underflow

`test_stack_underflow` — PRINT nua. TODO `XDBG-ERR-01`.

## Caso 14: memory out of bounds

`test_memory_out_of_bounds` — `bad_mem.asm`. TODO `XDBG-ERR-01` /
`XDBG-MEM-01`. Mutante `MUTANT-NO-BOUNDS`.

## Caso 15: return stack underflow

`test_return_stack_underflow` — `bad_ret.asm`. TODO `XDBG-ERR-01`.
