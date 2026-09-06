# CLVM binary format (ISA estendida — Dia 04)

Header v1 inalterado (`version=1`, `flags=0`). Opcodes além da base Dia 01:

| Opcode | Mnemonic | Operands | Efeito |
|---:|---|---|---|
| 0x0B | CALL | i16 relativo | push return-PC; PC ← alvo |
| 0x0C | RET | — | pop return-PC → PC |
| 0x0D | LOAD | — | `addr -- value` (i32 LE, mem 256 B) |
| 0x0E | STORE | — | `value addr --` |
| 0x0F | DROP | — | `a --` |
| 0x10 | SWAP | — | `a b -- b a` |
| 0x11 | EQ | — | `a b -- (a==b ? 1 : 0)` |
| 0x12 | LT | — | `a b -- (a<b ? 1 : 0)` signed |
| 0x13 | JNZ | i16 relativo | `cond --`; jump se cond ≠ 0 |

Deslocamento de JMP/JZ/CALL/JNZ: medido a partir do PC **após** o i16.
Call stack separada da data stack. Memória linear runtime: 256 bytes (não no header).
