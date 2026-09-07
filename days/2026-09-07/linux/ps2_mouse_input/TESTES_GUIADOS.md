# Testes guiados — PS/2 mouse input

### Caso 1: Compile e execute `ps2_mouse_test` em starter/ (falha até implementar TODOs).
### Caso 2: **Decode:** `move_right_up.raw` → dx=5, dy=3.
### Caso 3: **Map:** dois eventos REL + BTN_LEFT press.
### Caso 4: **Release:** `buttons_up.raw` → BTN_LEFT value 0.
### Caso 5: **Ring:** 32 pushes OK, 33º retorna -1.
### Caso 6: Valide solutions/ com os mesmos asserts.

## PS2-MOUSE-DECODE-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: PS2-MOUSE-DECODE-01`.

## PS2-MOUSE-EVENT-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: PS2-MOUSE-EVENT-02`.

## PS2-MOUSE-RING-03

Invariante protegida pelo teste com `PEDAGOGY-TEST: PS2-MOUSE-RING-03`.

## PS2-MOUSE-READ-04

Invariante protegida pelo teste com `PEDAGOGY-TEST: PS2-MOUSE-READ-04`.

## Execução

```bash
cd days/2026-09-07/linux/ps2_mouse_input/starter
cmake -S . -B build
cmake --build build
./build/ps2_mouse_test
ctest --test-dir build
```

**Esperado:** `OK ps2 mouse input`

## Review opcional

Compare `chris_ps2_mouse.c` com `psmouse-base.c`: onde o kernel valida sync bit e reporta botões?
