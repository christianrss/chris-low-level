# Teoria passo a passo — Linux — HID boot keyboard → InputEvent

Módulo: `linux/hid_keyboard_boot`. Pipeline educacional: relatório bruto → decode → map → ring → read.

---

## Visão geral

```mermaid
flowchart LR
  USB[HID 8-byte report] --> DECODE[HID-KBD-DECODE-01]
  DECODE --> MAP[HID-KBD-MAP-02]
  MAP --> RING[HID-KBD-RING-03]
  RING --> READ[HID-KBD-READ-04]
  READ --> APP[userspace / evdev]
```

```
fixtures/report_a_press.raw
        ↓
hid_boot_parse_report()     → HidBootReport
        ↓
hid_kbd_map_events()        → InputEvent (EV_KEY)
        ↓
hid_kbd_ring_push/read()    → FIFO de eventos
        ↓
chris_hid_kbd.c (review)    → hid_driver + input_report_key no kernel
```

| Camada | O quê | Por quê existe |
|--------|-------|----------------|
| Relatório HID boot | 8 bytes fixos (modifiers + 6 keys) | Subset mínimo suportado por BIOS/firmware |
| `HidBootReport` | Estado parseado | Separa wire format de lógica de diff |
| `InputEvent` | 24 bytes, tipo/código/valor | Mesmo contrato que `/dev/input/event*` |
| `HidKbdRing` | Buffer circular 32 eventos | IRQ produz mais rápido que userspace consome |
| `read()` lógico | Drain FIFO | Espelha `evdev_read` sem syscall real |

---

## 1. Layout `InputEvent` (evdev simplificado)

Struct de **24 bytes** alinhada ao que userspace lê de `/dev/input/eventX`:

```c
typedef struct {
    uint64_t time_us;
    uint16_t type;
    uint16_t code;
    int32_t  value;
    uint64_t __pad;
} InputEvent;
```

- `type == EV_KEY (0x01)` com `code == KEY_A (30)` e `value == 1` = tecla pressionada.
- `value == 0` = solta.
- Timestamp simplificado em microssegundos (`hid_kbd_set_time`).

**Por quê este formato?** Drivers kernel não entregam “letra a” — entregam **eventos normalizados**. O subsistema input unifica teclado USB, PS/2 e virtuais no mesmo struct.

**Invariantes:** `sizeof(InputEvent) == 24`; ordem preservada no ring.

---

## 2. Relatório HID boot (8 bytes)

Formato **Boot Protocol**:

| Byte | Campo |
|------|-------|
| 0 | Modifiers (Ctrl, Shift, Alt, GUI — bits) |
| 1 | Reservado (0) |
| 2–7 | Até 6 **usage codes** pressionados (0 = slot vazio) |

Exemplo `report_a_press.raw`: `00 00 04 00 00 00 00 00` → usage `0x04` = tecla **A**.

`hid_boot_parse_report` copia byte 0 para `modifiers` e bytes 2–7 para `keys[6]` — só normaliza wire format.

**Por quê separar decode de map?** Testes unitários e camadas do kernel (`hidraw` → `hid-input`) ficam independentes; wire format não vaza para semântica Linux.

| Sintoma | Causa | Depuração |
|---------|-------|-----------|
| KEY errado | scancode PC vs HID usage | tabela `0x04` → `KEY_A` |
| Tecla “gruda” | sem `value=0` ao sumir | diff `prev` vs `cur` |

---

## 3. Mapeamento HID → `InputEvent` (HID-KBD-MAP-02)

Comparar relatório **atual** com **anterior** e emitir eventos só nas **transições**:

1. Bit de modifier que mudou → `EV_KEY` com `KEY_LEFTCTRL`, etc.
2. Usage `0x04..0x2C` conhecido: apareceu → `value=1`; sumiu → `value=0`.

**Por quê diff e não interpretar snapshot?** Relatórios HID boot são **estado instantâneo**, não eventos de borda. O driver calcula transições — igual `hidinput` no kernel.

Trace manual:
```
prev: keys=[]  cur: keys=[0x04]  → EV_KEY KEY_A value=1
prev: keys=[0x04]  cur: keys=[]  → EV_KEY KEY_A value=0
```

---

## 4. Ring buffer (HID-KBD-RING-03)

Fila circular fixa (`HID_KBD_RING_CAP = 32`). `push` rejeita quando `count == CAP` (`-1`); índices `head`/`tail` com módulo `CAP`.

Interrupção USB pode disparar dezenas de relatórios por segundo; userspace pode bloquear. Ring absorve picos — padrão em drivers reais (`kfifo`).

---

## 5. `read()` lógico (HID-KBD-READ-04)

`hid_kbd_ring_read(ring, out, max_out)` copia até `max_out` eventos e remove do ring. Espelha `read(fd, buf, len)` em evdev.

---

## 6. Fixtures

| Arquivo | Bytes (hex) | Significado |
|---------|-------------|-------------|
| `report_a_press.raw` | `00 00 04 00 00 00 00 00` | Tecla A pressionada |
| `report_empty.raw` | `00 00 00 00 00 00 00 00` | Nenhuma tecla |

---

## 7. `chris_hid_kbd.c` (review only)

Esqueleto de `hid_driver` com `probe`/`event`. Não compila no Windows — leitura crítica. Conecta o pipeline userspace a `drivers/hid/hid-input.c`.

| Lab userspace | Kernel real |
|---------------|-------------|
| `hid_boot_parse_report` | `hid_report_raw` |
| `hid_kbd_map_events` | `hidinput_hid_event` |
| `HidKbdRing` | waitqueue + fila |

---

## 8. Depuração correlacionada

```bash
cd starter && cmake -S . -B build && cmake --build build && ./build/hid_kbd_test
```

Ordem: decode → map → ring → read. Input bugs são “fantasmas” sem estado `prev` — logue par `(prev, cur)`.

---

## 9. Tabela HID usage → KEY (subset)

| HID usage | Linux code | Tecla |
|-----------|------------|-------|
| 0x04 | KEY_A (30) | A |
| 0x05 | KEY_B (48) | B |
| 0x28 | KEY_ENTER (28) | Enter |
| 0x2C | KEY_SPACE (57) | Space |

---

## 10. Resumo

| TODO | Entrega |
|------|---------|
| DECODE-01 | Wire → `HidBootReport` |
| MAP-02 | Diff → `InputEvent` |
| RING-03 | FIFO com overflow -1 |
| READ-04 | Drain ordenado |

Próximo passo: `EXERCICIOS.md` e implementação em `starter/hid_kbd.c`.
