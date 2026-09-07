# Linux input: HID boot keyboard → InputEvent → ring buffer → read()

**Objetivo:** Decodificar relatórios HID boot de 8 bytes, mapear para `InputEvent` (modelo evdev simplificado), enfileirar em ring buffer e expor via `read()` userspace — antes de revisar driver kernel real.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. `starter/`
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `HID-KBD-DECODE-01` — parse do relatório boot 8 bytes
- `HID-KBD-MAP-02` — transições press/release → `EV_KEY`
- `HID-KBD-RING-03` — push em ring buffer fixo
- `HID-KBD-READ-04` — drain FIFO via read

## Pipeline

```
fixtures/*.raw (8 bytes)
        ↓ hid_boot_parse_report
HidBootReport (modifiers + 6 key slots)
        ↓ hid_kbd_map_events (diff vs prev)
InputEvent[24] (EV_KEY, KEY_*, value 0|1)
        ↓ hid_kbd_ring_push
HidKbdRing (cap 32)
        ↓ hid_kbd_ring_read
userspace consumer (test / evdev mental model)
```

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-linux-input-lab/day07` |
| O que levar | `hid_kbd` userspace + notas de review |
| Testes a replicar | `hid_kbd_test` |
| Milestone | input lab milestone |
| Commit sugerido | `feat(input): port hid boot keyboard from day07 lab` |
