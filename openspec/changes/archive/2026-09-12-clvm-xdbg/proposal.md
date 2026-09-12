# Proposal: Day 2026-09-12 — mini xdbg da CLVM

## Problem

O Dia 04 deixou a ISA estendida (CALL/RET, memória, comparações) como
alvo, mas o aluno não constrói um observador do estado. Um x64dbg nativo
(anexar processo Windows, disasm x86-64) não cabe em 6–8 h nem no CI
Linux. Falta um debugger in-process da CLVM: hex, disasm, step, pilhas
e RAM.

## Solution

Publicar `days/2026-09-12/` no perfil `depth_first`, lane `systems`,
ciclo `depth-core-01`, com um único projeto `systems/clvm_xdbg`.

O aluno implementa sessão de debug sobre a imagem CLVM v1 + opcodes
estendidos do Dia 04. O assembler e o loader são infraestrutura. O
núcleo student-owned é fetch/decode/execute observável, views e falhas.

O Dia 04 recebe apenas o conserto cirúrgico do starter desonesto; a
pedagogia nova vive neste dia.

## Reference

- `days/2026-09-03/systems/clvm/` — loader, formato, starters vazios
- `days/2026-09-04/systems/clvm_extended/docs/FORMAT.md` — ISA alvo
- `openspec/specs/day-contract/cycles/depth-core-01.yaml`

## Success criteria

- `day.contract.yaml`: `profile: depth_first`, 6–8 h, `systems`, `depth-core-01`
- Pacote canônico + `ASSESSMENT.yaml` + `RUBRIC.md`
- Gates: pedagogy, day contract, starter `--expect-fail`, solutions,
  mutantes, `cycle_contract_check.py --cycle depth-core-01`
- Sem GUI Win32
