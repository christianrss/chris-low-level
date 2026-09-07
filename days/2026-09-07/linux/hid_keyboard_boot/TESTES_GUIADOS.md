# Testes guiados — HID boot keyboard

### Caso 1: Compile e execute `hid_kbd_test` em starter/ (falha até implementar TODOs).
### Caso 2: `sizeof(InputEvent)==24` — layout evdev simplificado.
### Caso 3: **Decode:** `report_a_press.raw` → `keys[0]==0x04`.
### Caso 4: **Map:** press→release gera `KEY_A` value 1 depois 0.
### Caso 5: **Ring:** overflow após 32 pushes retorna -1.
### Caso 6: Valide solutions/ com os mesmos asserts.

## HID-KBD-DECODE-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: HID-KBD-DECODE-01`.

## HID-KBD-MAP-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: HID-KBD-MAP-02`.

## HID-KBD-RING-03

Invariante protegida pelo teste com `PEDAGOGY-TEST: HID-KBD-RING-03`.

## HID-KBD-READ-04

Invariante protegida pelo teste com `PEDAGOGY-TEST: HID-KBD-READ-04`.

## Execução

```bash
cd days/2026-09-07/linux/hid_keyboard_boot/starter
cmake -S . -B build
cmake --build build
./build/hid_kbd_test
ctest --test-dir build
```

**Esperado após TODOs:** `OK hid keyboard boot`

## Review opcional

Leia `starter/chris_hid_kbd.c` e liste três gaps vs driver de produção (sync, botões, registro de input_dev).
