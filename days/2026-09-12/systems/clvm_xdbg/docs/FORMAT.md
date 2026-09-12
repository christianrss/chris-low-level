# CLVM v1 + ISA estendida (alvo do xdbg)

All multibyte integers are little-endian. Header size is 16 bytes.

## Header

| Offset | Size | Field | Meaning |
|---:|---:|---|---|
| 0x00 | 4 | magic | ASCII `CLVM` |
| 0x04 | 1 | version | must be 1 |
| 0x05 | 1 | flags | reserved; must be 0 |
| 0x06 | 2 | entry | initial bytecode PC |
| 0x08 | 4 | code_size | number of bytecode bytes |
| 0x0C | 4 | checksum | FNV-1a 32-bit over code bytes |

File size must be exactly `16 + code_size`.

## Bytecode (Dia 01 + Dia 04)

| Opcode | Mnemonic | Operands | Stack / control |
|---:|---|---|---|
| 0x01 | PUSH | i32 LE | `-- value` |
| 0x02 | ADD | — | `a b -- a+b` |
| 0x03 | SUB | — | `a b -- a-b` |
| 0x04 | MUL | — | `a b -- a*b` |
| 0x05 | DIV | — | `a b -- a/b` |
| 0x06 | DUP | — | `a -- a a` |
| 0x07 | PRINT | — | `a --` (debugger guarda em `prints`) |
| 0x08 | HALT | — | status=halted |
| 0x09 | JMP | i16 relativo | PC ← PC_após_i16 + disp |
| 0x0A | JZ | i16 relativo | `cond --`; jump se 0 |
| 0x0B | CALL | i16 relativo | push return-PC; jump |
| 0x0C | RET | — | pop return-PC → PC |
| 0x0D | LOAD | — | `addr -- value` (i32 LE, mem 256 B) |
| 0x0E | STORE | — | `value addr --` |
| 0x0F | DROP | — | `a --` |
| 0x10 | SWAP | — | `a b -- b a` |
| 0x11 | EQ | — | `a b -- (a==b ? 1 : 0)` |
| 0x12 | LT | — | `a b -- (a<b ? 1 : 0)` signed |
| 0x13 | JNZ | i16 relativo | `cond --`; jump se ≠ 0 |

Deslocamento de JMP/JZ/CALL/JNZ: medido a partir do PC **após** o i16.
Call stack separada da data stack. Memória linear runtime: 256 bytes
(não está no header).
