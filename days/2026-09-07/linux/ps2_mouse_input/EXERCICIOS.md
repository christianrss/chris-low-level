# Exercícios — PS/2 mouse input

## Fácil — PS2-MOUSE-DECODE-01
Implemente `ps2_mouse_decode()` com sign extension nos eixos X e Y. `move_right_up.raw` deve resultar em `dx=5`, `dy=3`.

## Médio — PS2-MOUSE-EVENT-02
Implemente `ps2_mouse_map_events()` emitindo `REL_X` e `REL_Y` quando não zero, e `EV_KEY` para transições de botão.

## Médio — PS2-MOUSE-RING-03
Implemente `ps2_mouse_ring_push()` — mesma semântica do lab HID (cap 32, `-1` se cheio).

## Difícil — PS2-MOUSE-READ-04
Implemente `ps2_mouse_ring_read()` e valide sequência move + botão esquerdo no teste integrado.

## Desafio
Suporte movimento negativo: crie fixture `move_left.raw` com byte1=0xFD e bit4=1 em byte0; assert `dx==-3`.

## Reflexão
Por que PS/2 entrega movimento relativo enquanto touchscreen usa `EV_ABS`? Quando você escolheria cada modelo?
