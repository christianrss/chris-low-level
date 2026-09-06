# Teoria passo a passo — CLVM extended (CLVM-EXT)

## 1. O que estamos construindo

A ISA do Dia 01 (aritmética, JMP/JZ) ganha **procedures**, **memória linear**, **comparações** e **ops de stack**. Com isso você escreve loops, `if`, funções e variáveis em slots — sem truques.

TODOs: `CLVM-EXT-01` (assembler), `CLVM-EXT-02` (CALL/RET), `CLVM-EXT-03` (LOAD/STORE+bounds), `CLVM-EXT-04` (DROP/SWAP/EQ/LT/JNZ + `max_loop`).

## 2. Por que um lab só

Separar CALL e memória em dias diferentes força o aluno a reabrir a VM duas vezes. Aqui o salto pedagógico é **uma ISA utilizável** ao lado da JS bytecode VM do mesmo dia.

## 3. Mapa de opcodes novos

| Hex | Nome | Stack / efeito |
|-----|------|----------------|
| 0x0B | CALL | push return-PC; jump relativo |
| 0x0C | RET | pop return-PC |
| 0x0D | LOAD | addr → value |
| 0x0E | STORE | value, addr → |
| 0x0F | DROP | descarta topo |
| 0x10 | SWAP | troca dois topos |
| 0x11 | EQ | a==b → 0/1 |
| 0x12 | LT | a<b → 0/1 (signed) |
| 0x13 | JNZ | jump se ≠ 0 |

### Por que call stack separada

Se misturar return-PC com dados, um `ADD` errado corrompe o retorno. Duas stacks = contrato claro (como RISC-V `ra` vs operandos).

## 4. CALL/RET — CLVM-EXT-02

```text
CALL label:
  1. ler i16; pc aponta após o operando
  2. push pc na call_stack
  3. pc ← pc + relative

RET:
  1. se call_stack vazia → "return stack underflow"
  2. pc ← pop(call_stack)
```

Programa `add2.asm`: `PUSH 3; PUSH 5; CALL add2; PRINT; HALT` / `add2: ADD; RET` → stdout `8`.

### Por que displacement igual ao JMP

Mesma convenção = um único `checked_jump` e labels no assembler.

## 5. Memória linear — CLVM-EXT-03

```text
mem[0..255] zerada no boot
ok ⇔ addr >= 0 && addr + 4 <= 256
STORE: pop addr, pop value → LE32
LOAD:  pop addr → push LE32
```

`mem_demo.asm` grava 42 em `@0` e imprime. `bad_mem.asm` (STORE `@254`) → `memory out of bounds`.

### Por que 256 bytes fixos

Lab educacional: bounds trivial, sem mmap. Capstone pode crescer depois.

## 6. Comparações e loops — CLVM-EXT-04

```text
LT: pop b, pop a → push (a < b ? 1 : 0)
EQ: idem com ==
JNZ: pop cond; se ≠ 0, jump relativo
SWAP: a b → b a
DROP: descarta
```

`max_loop.asm` conta `0..3` em `mem[0]` com `LT`+`JNZ`, depois `SWAP`/`DROP`/`EQ` imprime `1`.

### Por que LT em vez de só JZ

Com só `JZ` você testa “é zero?”. `LT`/`EQ` + `JNZ`/`JZ` modelam `while (i < n)` e `if (a == b)` direto.

## 7. Assembler — CLVM-EXT-01

Mnemonics sem operando: `RET LOAD STORE DROP SWAP EQ LT`.
Com label (i16): `JMP JZ CALL JNZ`.
Tamanhos: PUSH=5, branch=3, resto=1.

## 8. Paper-trace rápido (max_loop início)

| passo | stack (topo→) | mem[0] | stdout |
|-------|---------------|--------|--------|
| STORE 0 | | 0 | |
| LOAD; DUP; PRINT | 0 | 0 | 0 |
| ADD 1; STORE | | 1 | |
| … até i=3 | | 4 | 0 1 2 3 |
| SWAP/DROP/EQ | 1 | | 1 |

## 9. Erros obrigatórios

| Situação | Mensagem |
|----------|----------|
| RET sem frame | `return stack underflow` |
| LOAD/STORE OOB | `memory out of bounds` |
| stack vazia em op | `stack underflow` |

## 10. Ligação com o Dia 01

Header, FNV checksum, PUSH/ADD/…/JMP/JZ **não mudam**. Programas `arithmetic.asm` ainda imprimem `38`.

## 11. Capstone

Porte tudo para `projects/chris-vm` (mesmo FORMAT). Próximos no ROADMAP: verifier, debugger, JIT — não neste lab.

## 12. Checklist mental antes do código

1. Labels resolvidos em dois passes?
2. CALL empurra PC **após** o i16?
3. STORE ordem `value addr` (addr no topo)?
4. LT signed (`int32_t`), não unsigned?
5. JNZ ≠ JZ (condição invertida)?

## 13. Próximo passo após o lab

Porte a ISA para `projects/chris-vm` e rode os mesmos programas lá — o FORMAT deve ser idêntico byte a byte.
