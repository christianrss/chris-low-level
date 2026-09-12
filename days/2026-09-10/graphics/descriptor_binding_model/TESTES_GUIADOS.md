# Testes guiados — descriptor_binding_model

### Caso 1: `GFX-DESC-LAYOUT`
`make_layout(3)` → `slot_count==3`; `make_layout(99)` clampa a `kMaxSlots`.

### Caso 2: `GFX-DESC-BIND`
Após bind RGB nos slots 0..2, `bound[i]` é true e `tints` guardam os valores.

### Caso 3: `GFX-DESC-SAMPLE`
`sample` devolve o tint bound; slot fora do layout/unbound devolve zero.

### Caso manual — VISUAL-01
Abra `desc_sw` e `desc_gl`. Três painéis lado a lado (vermelho/verde/azul inicial) sobem/descem levemente; a cada ~1.5s as cores rotacionam entre os painéis via rebind. Esc fecha. Mesma cena nos dois backends.
