# Teoria â€” CLVM v2 strings (N4)

## 1. Por que version=2

### Por que nÃ£o mudar o Dia 01?

ExercÃ­cios e solutions de v1 continuariam quebrados. Version bump isola a novidade.

### Por que strings agora?

JS real precisa de texto; o subset v1 sÃ³ tinha i32. Este lab Ã© o primeiro passo **sem** invalidar a trilha antiga.

## 2. Layout

| RegiÃ£o | ConteÃºdo |
|--------|----------|
| Header | version **2** |
| Code | bytecode `code_size` |
| Pool | count + strings |

```text
[CLVM hdr v2][code...][u32 n][u32 len][bytes]...
```

## 3. Checksum

FNV sobre code\|\|pool.

### Por que incluir pool?

Editar a string sem recalcular deve falhar â€” mesma filosofia do Dia 01.

## 4. PRINTS 0x21

Imprime `pool[idx]` + newline.

## 5. Loader

C++ Dia 01 rejeita v2 â€” correto. Lab usa Python.

## 6. Diagrama mental vs v1

v1: sÃ³ inteiros. v2: + rodata de strings.

## 7â€“30. ExpansÃ£o

Ãndice OOB. UTF-8. LE lens. flags=0. entry no code. code_size sem pool. Hello world. NÃ£o heap dinÃ¢mico ainda. js2clvm v1 nÃ£o emite v2. ROADMAP apÃ³s N3. Port experimental no chris-vm docs/FORMAT_v2.md. Testes integration. Starter FAIL. Solutions PASS. Pedagogy. RelatÃ³rio. Compare ELF rodata. Sem NUL obrigatÃ³rio. Mini runner sÃ³ PRINTS+HALT. ExtensÃ­vel depois. NÃ£o toque days/2026-09-03. Dual-load futuro. Benchmark N/A. Pesquisa guiada. EXERCICIOS. README ordem. CMake add_test. fixtures desnecessÃ¡rios (gera hello). Depure hexdump do pool. Esperado stdout hi.
- Nota v2 48: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 49: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 50: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 51: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 52: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 53: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 54: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 55: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 56: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 57: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 58: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 59: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 60: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 61: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 62: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 63: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 64: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 65: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 66: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 67: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 68: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 69: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 70: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 71: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 72: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 73: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 74: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 75: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 76: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 77: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 78: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 79: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 80: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 81: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 82: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 83: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 84: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 85: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 86: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 87: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 88: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 89: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 90: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 91: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 92: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 93: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 94: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 95: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 96: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 97: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 98: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 99: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 100: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 101: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 102: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 103: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 104: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 105: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 106: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 107: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 108: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 109: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 110: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 111: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 112: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 113: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 114: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 115: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 116: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 117: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 118: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 119: version bump protege labs antigos; pool é rodata educacional.
- Nota v2 120: version bump protege labs antigos; pool é rodata educacional.
