# Testes guiados

### Caso 1: `python starter/test_ansi.py` — importa `AnsiParser` (não `Terminal`).
### Caso 2: **SGR:** `\x1b[31m` define vermelho; `\x1b[0m` restaura fg=7.
### Caso 3: **Cursor:** `\x1b[10;20H` → row=9, col=19 (0-based).
### Caso 4: **Home:** `\x1b[H` → (0,0).
### Caso 5: **CSI incompleto:** `\x1b[` sem final → ValueError.
### Caso 6: Valide solutions/ com os mesmos testes.

## TERM-CURSOR-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: TERM-CURSOR-02`.

## TERM-ANSI-SGR-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: TERM-ANSI-SGR-01`.
