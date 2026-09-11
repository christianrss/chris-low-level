# Testes guiados

## Caso 1: `AI-ATTN-01`

causal_mask(2,2)==1 e (2,3)==0.

## Caso 2: `AI-ATTN-02`

apply_mask escreve −1e9 e retorna 0.

## Caso 3: `AI-ATTN-03`

visible_count(2)==3.

## Identificadores

- `AI-ATTN-01` — exercido pelo caso acima; o assert usa o valor da TEORIA.

- `AI-ATTN-02` — exercido pelo caso acima; o assert usa o valor da TEORIA.

- `AI-ATTN-03` — exercido pelo caso acima; o assert usa o valor da TEORIA.
