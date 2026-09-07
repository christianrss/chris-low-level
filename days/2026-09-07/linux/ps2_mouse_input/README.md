# Linux input: PS/2 mouse packet → REL/BTN InputEvent → ring buffer → read()

**Objetivo:** Decodificar pacotes PS/2 de 3 bytes, emitir eventos `EV_REL` e `EV_KEY` (botões), enfileirar no mesmo modelo `InputEvent` de 24 bytes e consumir via `read()`.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. `starter/`
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `PS2-MOUSE-DECODE-01` — parse do pacote 3 bytes + sign bits
- `PS2-MOUSE-EVENT-02` — `REL_X`/`REL_Y` + transições de botão
- `PS2-MOUSE-RING-03` — push em ring buffer
- `PS2-MOUSE-READ-04` — drain FIFO

## Pipeline

```
fixtures/*.raw (3 bytes)
        ↓ ps2_mouse_decode
Ps2MousePacket (dx, dy, buttons)
        ↓ ps2_mouse_map_events
InputEvent[24] (EV_REL / EV_KEY)
        ↓ ps2_mouse_ring_push
Ps2MouseRing
        ↓ ps2_mouse_ring_read
userspace consumer
```

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-linux-input-lab/day07` |
| O que levar | `ps2_mouse` userspace + review `chris_ps2_mouse.c` |
| Testes a replicar | `ps2_mouse_test` |
| Commit sugerido | `feat(input): port ps2 mouse from day07 lab` |
