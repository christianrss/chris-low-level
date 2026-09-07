# Resolução guiada passo a passo — Linux — HID boot keyboard

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `HID-KBD-DECODE-01` | `starter/hid_kbd.c` | `hid_boot_parse_report` | stub `TODO [HID-KBD-DECODE-01]` |
| `HID-KBD-MAP-02` | `starter/hid_kbd.c` | `hid_kbd_map_events` | stub `TODO [HID-KBD-MAP-02]` |
| `HID-KBD-RING-03` | `starter/hid_kbd.c` | `hid_kbd_ring_push` | stub `TODO [HID-KBD-RING-03]` |
| `HID-KBD-READ-04` | `starter/hid_kbd.c` | `hid_kbd_ring_read` | stub `TODO [HID-KBD-READ-04]` |

> Trabalhe em `days/2026-09-07/linux/hid_keyboard_boot/starter/`.

---

## Baseline

```bash
cd days/2026-09-07/linux/hid_keyboard_boot/starter
cmake -S . -B build && cmake --build build && ./build/hid_kbd_test
```

**Esperado antes dos TODOs:** compila, asserts falham (parse, map, ring, read).

---

## HID-KBD-DECODE-01 — `hid_boot_parse_report`

### Onde colocar (DECODE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hid_kbd.c` |
| Função | `hid_boot_parse_report` |
| Substituir | corpo com `TODO [HID-KBD-DECODE-01]` |

### 1. O problema (DECODE-01)

O relatório HID boot tem 8 bytes com byte 1 reservado. Sem copiar bytes 0 e 2–7 corretamente, `keys[0]` nunca recebe `0x04` da fixture `report_a_press.raw`.

### Escreva o código (DECODE-01)

```c
void hid_boot_parse_report(const uint8_t raw[8], HidBootReport* out) {
    out->modifiers = raw[0];
    out->keys[0] = raw[2];
    out->keys[1] = raw[3];
    out->keys[2] = raw[4];
    out->keys[3] = raw[5];
    out->keys[4] = raw[6];
    out->keys[5] = raw[7];
}
```

### Por que funciona (DECODE-01)

Byte 1 é reservado no boot protocol; slots de tecla começam em offset 2.

### Verifique (DECODE-01)

`report_a_press.raw` → `modifiers=0`, `keys[0]=0x04`. Assert de decode passa; map ainda falha.

---

## HID-KBD-MAP-02 — `hid_kbd_map_events`

### Onde colocar (MAP-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hid_kbd.c` |
| Função | `hid_kbd_map_events` |
| Substituir | stub `TODO [HID-KBD-MAP-02]` e helpers ausentes |

### 1. O problema (MAP-02)

HID boot entrega snapshot de teclas pressionadas, não eventos de release explícitos. Comparar `cur` com `prev` gera `EV_KEY` com `value=1` na borda de press e `value=0` na borda de release.

### Escreva o código (MAP-02)

Implemente `hid_usage_to_key`, `key_in_report` e o loop de diff (modifiers + usages 0x04..0x2C). Preencha `time_us`, `type=EV_KEY`, `code`, `value`, `__pad=0` em cada evento emitido.

### Por que funciona (MAP-02)

Tecla que some do array implica release; modifier que muda de bit gera evento de borda.

### Verifique (MAP-02)

Asserts de `KEY_A` press/release passam; ring ainda falha.

### Debug (MAP-02)

| Sintoma | Causa | Ação |
|---------|-------|------|
| release ausente | falta branch `!cur_on && prev_on` | compare com `prev` |
| modifier ignorado | só iterou `keys[]` | cheque byte 0 |

---

## HID-KBD-RING-03 — `hid_kbd_ring_push`

### Onde colocar (RING-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hid_kbd.c` |
| Função | `hid_kbd_ring_push` |
| Substituir | stub `TODO [HID-KBD-RING-03]` |

### 1. O problema (RING-03)

IRQ pode enfileirar eventos mais rápido que o consumidor lê. Sem ring, eventos se perdem; com ring cheio, `push` deve retornar `-1` explicitamente.

### Escreva o código (RING-03)

```c
int hid_kbd_ring_push(HidKbdRing* ring, const InputEvent* ev) {
    if (ring->count >= HID_KBD_RING_CAP) return -1;
    ring->buf[ring->tail] = *ev;
    ring->tail = (ring->tail + 1) % HID_KBD_RING_CAP;
    ++ring->count;
    return 0;
}
```

### Por que funciona (RING-03)

Escrita em `tail`, avanço circular, `count` rastreia ocupação.

### Verifique (RING-03)

Push duplo preserva ordem; terceiro push com capacidade 2 retorna `-1`.

---

## HID-KBD-READ-04 — `hid_kbd_ring_read`

### Onde colocar (READ-04)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hid_kbd.c` |
| Função | `hid_kbd_ring_read` |
| Substituir | stub `TODO [HID-KBD-READ-04]` |

### 1. O problema (READ-04)

Userspace lê lotes de eventos via `read()`. `hid_kbd_ring_read` deve drenar FIFO de `head`, copiando até `max_out` eventos.

### Escreva o código (READ-04)

```c
ssize_t hid_kbd_ring_read(HidKbdRing* ring, InputEvent* out, size_t max_out) {
    size_t n = 0;
    while (n < max_out && ring->count > 0) {
        out[n] = ring->buf[ring->head];
        ring->head = (ring->head + 1) % HID_KBD_RING_CAP;
        --ring->count;
        ++n;
    }
    return (ssize_t)n;
}
```

### Por que funciona (READ-04)

Simétrico ao push — FIFO garantido.

### Verifique (READ-04)

Após dois push, read com `max_out=2` retorna ordem idêntica à inserção.

### Debug (READ-04)

| Sintoma | Causa | Ação |
|---------|-------|------|
| ordem invertida | head/tail trocados | push em tail, read de head |
| count negativo | decremento sem checar | só leia se `count > 0` |

---

## Validação final

```bash
cmake --build build && ./build/hid_kbd_test
```

**Esperado:** `OK hid keyboard boot`

---

## Relatório de resolução

| Campo | Preencher |
|-------|-----------|
| TODOs concluídos | DECODE-01, MAP-02, RING-03, READ-04 |
| Primeira falha | |
| Bug mais difícil | |
| Evidência | `OK hid keyboard boot` |
