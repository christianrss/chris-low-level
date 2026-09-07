# Resolução guiada passo a passo — Linux — PS/2 mouse input

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `PS2-MOUSE-DECODE-01` | `starter/ps2_mouse.c` | `ps2_mouse_decode` | stub `TODO [PS2-MOUSE-DECODE-01]` |
| `PS2-MOUSE-EVENT-02` | `starter/ps2_mouse.c` | `ps2_mouse_map_events` | stub `TODO [PS2-MOUSE-EVENT-02]` |
| `PS2-MOUSE-RING-03` | `starter/ps2_mouse.c` | `ps2_mouse_ring_push` | stub `TODO [PS2-MOUSE-RING-03]` |
| `PS2-MOUSE-READ-04` | `starter/ps2_mouse.c` | `ps2_mouse_ring_read` | stub `TODO [PS2-MOUSE-READ-04]` |

> Trabalhe em `starter/`.

---

## Baseline

```bash
cd days/2026-09-07/linux/ps2_mouse_input/starter
cmake -S . -B build && cmake --build build && ./build/ps2_mouse_test
```

**Esperado antes dos TODOs:** compila, asserts falham (dx/dy zero, map retorna -1).

---

## PS2-MOUSE-DECODE-01 — `ps2_mouse_decode`

### Onde colocar (DECODE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ps2_mouse.c` |
| Função | `ps2_mouse_decode` |
| Substituir | stub `TODO [PS2-MOUSE-DECODE-01]` |

### 1. O problema (DECODE-01)

Pacote PS/2 codifica movimento em 8 bits com bit de sinal no byte 0. Sem sign extension, movimentos negativos aparecem como valores grandes positivos.

### Escreva o código (DECODE-01)

```c
void ps2_mouse_decode(const uint8_t pkt[3], Ps2MousePacket* out) {
    uint8_t flags = pkt[0];
    out->buttons = flags & 0x07;
    int dx = (int)pkt[1];
    int dy = (int)pkt[2];
    if (flags & 0x10) dx -= 256;
    if (flags & 0x20) dy -= 256;
    out->dx = dx;
    out->dy = dy;
}
```

### Por que funciona (DECODE-01)

Bits 4–5 do byte 0 são sign em complemento de 9 bits.

### Verifique (DECODE-01)

`move_right_up.raw` (`08 05 03`) → dx=5, dy=3, buttons=0.

---

## PS2-MOUSE-EVENT-02 — `ps2_mouse_map_events`

### Onde colocar (EVENT-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ps2_mouse.c` |
| Função | `ps2_mouse_map_events` |
| Substituir | stub `TODO [PS2-MOUSE-EVENT-02]` |

### 1. O problema (EVENT-02)

Um pacote pode gerar até cinco eventos: REL_X, REL_Y e até três transições de botão. Ordem do lab: REL_X, REL_Y, depois botões com diff vs `prev`.

### Escreva o código (EVENT-02)

Emita `EV_REL` para eixos não-zero; para cada bit de botão que mudou, `EV_KEY` com `value` 0 ou 1. Preencha `time_us`, `__pad=0`.

### Por que funciona (EVENT-02)

REL é delta por pacote; botões exigem borda como no HID.

### Verifique (EVENT-02)

Asserts de REL_X, REL_Y, BTN_LEFT passam.

### Debug (EVENT-02)

| Sintoma | Causa | Ação |
|---------|-------|------|
| 3 REL em vez de 2 | emitiu com dx=0 | cheque `!= 0` |
| BTN não solta | não comparou `prev` | diff de `buttons` |

---

## PS2-MOUSE-RING-03 — `ps2_mouse_ring_push`

### Onde colocar (RING-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ps2_mouse.c` |
| Função | `ps2_mouse_ring_push` |
| Substituir | stub `TODO [PS2-MOUSE-RING-03]` |

### 1. O problema (RING-03)

IRQ entrega pacotes mais rápido que o consumidor lê. Ring de 32 slots absorve picos; overflow retorna `-1`.

### Escreva o código (RING-03)

```c
int ps2_mouse_ring_push(Ps2MouseRing* ring, const InputEvent* ev) {
    if (ring->count >= PS2_MOUSE_RING_CAP) return -1;
    ring->buf[ring->tail] = *ev;
    ring->tail = (ring->tail + 1) % PS2_MOUSE_RING_CAP;
    ++ring->count;
    return 0;
}
```

### Por que funciona (RING-03)

Mesmo padrão do lab HID — reutilize o modelo mental.

### Verifique (RING-03)

Dois push + read preservam ordem FIFO.

---

## PS2-MOUSE-READ-04 — `ps2_mouse_ring_read`

### Onde colocar (READ-04)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ps2_mouse.c` |
| Função | `ps2_mouse_ring_read` |
| Substituir | stub `TODO [PS2-MOUSE-READ-04]` |

### 1. O problema (READ-04)

Consumidor precisa drenar eventos enfileirados sem perder ordem — espelha `read()` em evdev.

### Escreva o código (READ-04)

```c
ssize_t ps2_mouse_ring_read(Ps2MouseRing* ring, InputEvent* out, size_t max_out) {
    size_t n = 0;
    while (n < max_out && ring->count > 0) {
        out[n] = ring->buf[ring->head];
        ring->head = (ring->head + 1) % PS2_MOUSE_RING_CAP;
        --ring->count;
        ++n;
    }
    return (ssize_t)n;
}
```

### Por que funciona (READ-04)

Leitura de `head` simétrica ao push em `tail`.

### Verifique (READ-04)

`buttons_up.raw` após `left_down` gera BTN_LEFT value=0 no drain.

### Debug (READ-04)

| Sintoma | Causa | Ação |
|---------|-------|------|
| read retorna 0 com eventos | head/tail invertidos | push tail, read head |
| ordem errada | módulo CAP ausente | `% PS2_MOUSE_RING_CAP` |

---

## Validação final

```bash
cmake --build build && ./build/ps2_mouse_test
```

**Esperado:** `OK ps2 mouse input`

---

## Relatório de resolução

| Campo | Preencher |
|-------|-----------|
| TODOs concluídos | DECODE-01, EVENT-02, RING-03, READ-04 |
| Evidência | `OK ps2 mouse input` |
