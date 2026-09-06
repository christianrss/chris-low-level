# CLVM v1 binary format (extended)

All multibyte integers are little-endian.

## Header (16 bytes)

| Offset | Size | Field | Meaning |
|---:|---:|---|---|
| 0x00 | 4 | magic | ASCII `CLVM` |
| 0x04 | 1 | version | must be 1 |
| 0x05 | 1 | flags | reserved; must be 0 |
| 0x06 | 2 | entry | initial bytecode PC |
| 0x08 | 4 | code_size | number of bytecode bytes |
| 0x0C | 4 | checksum | FNV-1a 32-bit over code bytes |

The file size must be exactly `16 + code_size` bytes.

## Bytecode

| Opcode | Mnemonic | Operands | Stack effect |
|---:|---|---|---|
| 0x01 | PUSH | i32 little-endian | `-- value` |
| 0x02 | ADD | none | `a b -- a+b` |
| 0x03 | SUB | none | `a b -- a-b` |
| 0x04 | MUL | none | `a b -- a*b` |
| 0x05 | DIV | none | `a b -- a/b` |
| 0x06 | DUP | none | `a -- a a` |
| 0x07 | PRINT | none | `a --` |
| 0x08 | HALT | none | stops execution |
| 0x09 | JMP | signed i16 relative | changes PC |
| 0x0A | JZ | signed i16 relative | `cond --`; jump when cond == 0 |
| 0x0B | CALL | signed i16 relative | push return-PC; jump |
| 0x0C | RET | none | pop return-PC → PC |
| 0x0D | LOAD | none | `addr -- value` (i32 LE in 256 B linear mem) |
| 0x0E | STORE | none | `value addr --` |
| 0x0F | DROP | none | `a --` |
| 0x10 | SWAP | none | `a b -- b a` |
| 0x11 | EQ | none | `a b -- (a==b ? 1 : 0)` |
| 0x12 | LT | none | `a b -- (a<b ? 1 : 0)` signed |
| 0x13 | JNZ | signed i16 relative | `cond --`; jump when cond != 0 |

For JMP/JZ/CALL/JNZ, displacement is from the PC immediately after the i16 operand.
Return addresses use a call stack separate from the data stack.
Runtime linear memory is 256 bytes (not stored in the file header).

Lab source: `days/2026-09-04/systems/clvm_extended`.
