# Exercícios — parser ANSI/CSI

## Fácil

- **TERM-GRID-01:** escreva caracteres imprimíveis em `Ground` preservando cursor.
- **TERM-CSI-01:** movimentos CSI A/B/C/D com `param_or(1)` default.

## Médio

- **TERM-FEED-01:** estados `Escape` e `Csi` sob feeds parciais.
- **TERM-CLEAR-01:** `CSI 2 J` limpa grade e reseta cursor.

## Difícil

- **TERM-SPLIT-01:** mesmo teste com `feed()` dividido em 1 byte por chamada.
- **TERM-BOUNDS-01:** cursor nunca sai da grade após sequências longas.

## Desafio

- **TERM-SGR-01:** esboce extensão para `CSI 31 m` sem quebrar estados atuais.
