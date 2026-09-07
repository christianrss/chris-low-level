# Exercícios — HID boot keyboard

## Fácil — HID-KBD-DECODE-01
Implemente `hid_boot_parse_report()` para preencher `modifiers` e `keys[6]` a partir dos 8 bytes. Valide com `report_a_press.raw` (`keys[0]==0x04`).

## Médio — HID-KBD-MAP-02
Implemente `hid_kbd_map_events()` comparando `cur` e `prev`. Pressionar A deve gerar `EV_KEY`/`KEY_A`/`value=1`; soltar deve gerar `value=0`.

## Médio — HID-KBD-RING-03
Implemente `hid_kbd_ring_push()` com capacidade 32. Retorne `-1` quando cheio.

## Difícil — HID-KBD-READ-04
Implemente `hid_kbd_ring_read()` drenando em ordem FIFO. O teste empilha press+release e espera dois eventos na ordem correta.

## Desafio
Adicione suporte a modifier Left Ctrl (byte0 bit0) e teste transição press/release do `KEY_LEFTCTRL`.

## Reflexão
Compare o diff `prev/cur` do lab com o que `evtest` mostra ao segurar uma tecla física — por que múltiplos `EV_KEY` podem aparecer para uma única tecla em drivers reais?
