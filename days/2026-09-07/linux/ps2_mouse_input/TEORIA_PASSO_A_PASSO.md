# Teoria passo a passo — Linux — PS/2 mouse → InputEvent

Módulo: `linux/ps2_mouse_input`. Mesmo modelo `InputEvent` de 24 bytes, fonte diferente: pacote serial PS/2 de 3 bytes.

---

## Visão geral

```mermaid
flowchart LR
  PS2[PS/2 3-byte packet] --> DECODE[PS2-MOUSE-DECODE-01]
  DECODE --> MAP[PS2-MOUSE-EVENT-02]
  MAP --> RING[PS2-MOUSE-RING-03]
  RING --> READ[PS2-MOUSE-READ-04]
  READ --> APP[userspace / evdev]
```

| Camada | O quê | Por quê |
|--------|-------|---------|
| Pacote PS/2 | 3 bytes por movimento/botão | Protocolo IBM PC clássico |
| `Ps2MousePacket` | dx, dy, buttons | Estado após sign extension |
| `EV_REL` | REL_X, REL_Y com delta | Mouse é relativo |
| `EV_KEY` | BTN_LEFT/RIGHT/MIDDLE | Botões como teclas |
| Ring + read | Igual ao lab HID | Mesmo consumidor evdev |

---

## 1. `InputEvent` compartilhado

Mesmo header `input_event.h` do módulo HID — **24 bytes**. Movimento: `type=EV_REL`, `code=REL_X`/`REL_Y`, `value=delta`. Botão: `type=EV_KEY`, `code=BTN_LEFT`, `value=0|1`.

**Por quê o mesmo struct?** Compositores Wayland/X11 leem teclado e mouse do mesmo `/dev/input/event*` — unificar o tipo simplifica o consumidor.

---

## 2. Formato do pacote PS/2 (3 bytes)

| Byte | Bits | Significado |
|------|------|-------------|
| 0 | 0–2 | Botões esq/dir/meio |
| 0 | 3 | **Sempre 1** (sync) |
| 0 | 4–5 | Sinal de X/Y |
| 1 | — | Movimento X (8 bits) |
| 2 | — | Movimento Y (8 bits) |

```c
buttons = pkt[0] & 0x07;
dx = pkt[1];  if (pkt[0] & 0x10) dx -= 256;
dy = pkt[2];  if (pkt[0] & 0x20) dy -= 256;
```

**Por quê sign extension?** Movimento é complemento de dois em 9 bits. Sem `-256`, `0xFD` viraria +253 em vez de -3.

Fixture `move_right_up.raw` (`08 05 03`): dx=5, dy=3.

---

## 3. Mapeamento (PS2-MOUSE-EVENT-02)

1. `dx != 0` → `EV_REL` `REL_X`.
2. `dy != 0` → `EV_REL` `REL_Y`.
3. Botão que mudou vs `prev` → `EV_KEY` com `value` 0 ou 1.

Movimento é incremental por pacote; botões precisam de borda como no HID.

---

## 4. Ring buffer (PS2-MOUSE-RING-03)

`Ps2MouseRing` capacidade 32 — `push` rejeita quando cheio; `read` drena FIFO. Três bytes chegam em IRQ; userspace lê em lotes.

---

## 5. Read path (PS2-MOUSE-READ-04)

`ps2_mouse_ring_read` retorna quantos eventos copiou (0 se vazio). Mesmo algoritmo head/tail/count do teclado.

---

## 6. Fixtures

| Arquivo | Bytes | Efeito |
|---------|-------|--------|
| `move_right_up.raw` | `08 05 03` | dx=+5, dy=+3 |
| `left_down.raw` | `09 00 00` | botão esquerdo pressionado |
| `buttons_up.raw` | `08 00 00` | solta botões |

---

## 7. `chris_ps2_mouse.c` (review)

Driver `serio` mínimo — lacunas intencionais (sem botões, sem sync bit, sem `input_register_device`). Compare com `drivers/input/mouse/psmouse-base.c`.

---

## 8. PS/2 vs HID (mouse USB)

| Aspecto | PS/2 | USB HID |
|---------|------|---------|
| Transporte | IRQ serio | USB interrupt |
| Formato | 3 bytes fixos | report descriptor |
| Kernel | `psmouse` | `usbhid` |

Ambos convergem para `input_event`.

---

## 9. Convenção de eixo Y

PS/2: Y positivo geralmente = mover para **baixo**. No lab usamos valor bruto — drivers reais podem inverter conforme `INPUT_PROP`.

---

## 10. Depuração

```bash
cd starter && cmake -S . -B build && cmake --build build && ./build/ps2_mouse_test
```

Checklist: decode → map (2 REL + BTN) → ring FIFO → release em `buttons_up`.

---

## 11. Resumo

| TODO | Função | Entrega |
|------|--------|---------|
| DECODE-01 | `ps2_mouse_decode` | dx, dy, buttons |
| EVENT-02 | `ps2_mouse_map_events` | REL + BTN |
| RING-03 | `ps2_mouse_ring_push` | FIFO -1 overflow |
| READ-04 | `ps2_mouse_ring_read` | drain ordenado |

Implemente em `starter/ps2_mouse.c`.
