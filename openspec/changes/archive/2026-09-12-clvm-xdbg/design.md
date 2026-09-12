# Design: clvm_xdbg

## Forma

CLI de texto, testável por stdin. Sem anexar processo, sem x86-64.

```text
clvm-xdbg program.clvm
> hex          # header 16 B + code, offsets
> disasm       # mnemônico da instrução em PC
> regs         # PC, data stack, call stack
> mem 0 64     # hex da RAM 256 B
> step         # um opcode
> break <pc>
> continue
> quit
```

## Ownership

- Fornecido: `host/` (REPL, loader `clvm_parse`), `tools/assemble.py`,
  fixtures `.asm`, `include/session.hpp`.
- `student_owned`: `starter/src/**` — parse wiring, hex, disasm, step,
  snapshot, breakpoints, mensagens de erro.

## Contrato de step

Um `step` faz fetch/decode/execute de um opcode. Não existe `run()`
opaco. `continue` repete `step` até HALT, breakpoint (PC de destino,
sem reexecutar o PC de partida) ou erro.

Erros observáveis: truncamento da imagem, opcode desconhecido, stack
underflow, `memory out of bounds`, `return stack underflow`.

## Capstone

Views e step portam para `projects/chris-debugger`. A ISA permanece
em `projects/chris-vm`.
