# Testes guiados — input_event_entropy

## Caso 1 — `AI-EVT-ENT-01`

48 bytes iguais → entropia < 0.01.

## Caso 2 — `AI-EVT-RLE-02`

`[1,1,2]` → `[(1,2),(2,1)]`.

## Caso 3 — `AI-EVT-RATIO-03`

gzip ratio < 0.5 em dados repetitivos.

## Debug

| Falha | Causa |
|-------|-------|
| RLE vazio | não tratou `codes` vazio |
