# CLVM v2 — strings (lab N4)

**Não altera** Dia 01/04 (continuam em **v1**). Este módulo introduz `version == 2`.

## Layout do arquivo

Header 16 B igual ao v1, exceto `version = 2`.

| Região | Conteúdo |
|--------|----------|
| Header | magic `CLVM`, version **2**, flags 0, entry, code_size, checksum |
| Code | bytecode (`code_size` bytes) |
| Pool | `u32` count + para cada string: `u32` len + bytes UTF-8 |

Checksum FNV-1a: sobre **code \|\| pool** (diferente do v1, só code).

## Novos opcodes (v2 only)

| Op | Nome | Operands | Efeito |
|----|------|----------|--------|
| 0x21 | PRINTS | u16 index LE | imprime pool[index] + newline; sem stack |
| 0x22 | reserved | | |

Opcodes v1 (`0x01–0x13`) continuam válidos no code.

## TODOs

- `CLVM-V2-POOL-01` — parse/serialize do string pool
- `CLVM-V2-PRINTS-01` — emitir/executar `PRINTS`

## Teste

```powershell
cd solutions
python tests/integration_test.py
```

Esperado: programa que imprime `hi`.
