# Testes guiados — measurement_born

## Caso 1 — `Q-MEAS-01`

Após H em q0, `measure_probability(0)` e `(1)` ≈ 0.5.

## Caso 2 — `Q-MEAS-02`

`collapse_to(1)` → `probability(1)==1`.

## Caso 3 — `Q-BORN-03`

`born_select({0.5,0.5}, 0.25) == 1`.

## Debug

| Falha | Causa |
|-------|-------|
| P≠0.5 | H mal aplicado em 2-qubit |
