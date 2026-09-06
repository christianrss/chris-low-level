# Graphics reference — apêndice da resolução guiada

> Continuação de `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`. Use para traces extras, armadilhas de damage/vsync e sessão de debug.

## 1. Trace completo dirty AABB

Surface 8×8 preta.

```text
fill_rect(2,2,3,3) → clip ok → mark (2,2,3,3)
take_dirty_union → {2,2,3,3} area=9; tracker vazio

fill(0,0,2,2); fill(5,5,2,2)
union:
  x0=min(0,5)=0  y0=min(0,5)=0
  x1=max(2,7)=7  y1=max(2,7)=7
  → {0,0,7,7} area=49
```

Pixels “limpos” dentro da união (ex.: (3,3) se não foi pintado na segunda leva) ainda entram no damage — overdraw consciente da AABB.

## 2. Fantasma de sprite (bug clássico)

Sprite 16×16 em `(10,10)` move para `(14,10)`.

```text
errado:  mark só (14,10,16,16)
         → pixels em (10,10)-(13,25) ficam com o frame antigo (fantasma)

certo:   mark (10,10,16,16) ∪ (14,10,16,16)
         → union (10,10,20,16) cobre antigo e novo
```

O benchmark do lab marca footprints com folga (`ax-1`, `by-1`) por isso.

## 3. compose_with_damage vs compose

| | `Compositor::compose` | `FramePacer::compose_with_damage` |
|--|----------------------|-----------------------------------|
| Buffer | novo, preenchido com background | in-place no `target` |
| Escopo | tela inteira | `damage ∩ bounds` |
| Fora do damage | N/A (tudo novo) | **preserva** pixels antigos |
| Stats | — | `dirty_area`, `pixels_touched` |

Invariante de corretude: damage = bounds completos ⇒ mesmo resultado visual que `compose` (a menos do dirty tracker no output).

## 4. Sessão de debug — `pixels_touched == 0`

1. `damage` vazio ou totalmente fora dos bounds?
2. `intersect` devolveu empty (`width/height` ≤ 0)?
3. Passou `DirtyTracker` já limpo (double `take`)?

## 5. Sessão de debug — cor errada só no pace

1. Confira `sx = px - layer.x` (não `px + layer.x`).
2. Ordem das layers no sample deve ser a mesma do compose.
3. Background do pace deve ser o mesmo usado no compose de referência.

## 6. Vsync — orçamento numérico

```text
60 Hz → 1/60 ≈ 16.667 ms/frame
1080p RGBA8 ≈ 8.3 MB/frame full blit
damage 64x64 ≈ 16 KB → ~500× menos bytes tocados
```

Se o compose full leva 12 ms e o damage 0,4 ms, sobram ~16 ms para input/sim — pacing útil mesmo sem GPU.

## 7. Quando redesenhar full-screen

- União AABB cobre > ~70–80% da tela (threshold empírico).
- Mudança de tema / resize / first frame.
- Validação: compare checksum full vs damage full-rect.

## 8. Checklist final dos 6 TODOs

- [ ] INDEX throw + `y*width+x`
- [ ] FILL-RECT clip + `mark_dirty` pós-clip
- [ ] ALPHA-OVER `+127`
- [ ] COMPOSE z-order + footprint dirty
- [ ] DIRTY-RECT union + take limpa
- [ ] FRAME-PACE stats + preserva fora do damage

## 9. Relatório extra

- dirty_area mediano no benchmark damage: ___
- razão pixels_damage / pixels_full: ___
- fantasma reproduzido de propósito? Sim/Não
