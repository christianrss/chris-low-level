# Testes guiados — input_event_transform

## Caso 1 — `ND-INPUT-01`

Dois eventos de 24 bytes parseados.

## Caso 2 — `ND-INPUT-02`

1 byte residual no flush → erro.

## Caso 3 — `ND-INPUT-03`

`metrics().eventsParsed === 2`.

## Debug

| Falha | Causa |
|-------|-------|
| 0 eventos | faltou concat buffer |
