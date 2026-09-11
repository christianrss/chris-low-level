# Exercícios — input_event_ring_mux

## Fácil — paper-trace do Caso 1

Reproduza no papel o trace numérico da `TEORIA_PASSO_A_PASSO.md` (mesmos bytes/estados do teste).
Arquivo-alvo: nenhum (caderno). Critério de aceite: os números batem com `TESTES_GUIADOS.md` Caso 1 **antes** de editar código.

## Médio — `LIN-MUX-01`

Implemente `ring_push` em `starter/ring.c`.
Critério de aceite: o `PEDAGOGY-TEST` ligado a `LIN-MUX-01` PASS; valores iguais ao paper-trace.

## Difícil — `LIN-MUX-02` + `LIN-MUX-03`

Complete `ring_pop` e `mux_push` mantendo invariantes dos passos anteriores.
Critério de aceite: suíte completa do starter PASS; caso negativo (erro/bounds) ainda falha como documentado.

## Desafio — extensão sem quebrar testes

Altere apenas documentação ou um assert extra local: escolha um input *vizinho* ao Caso 1
(ex.: PUSH 256, 5º push no anel, id WASM 3, logits {1000,1001,1002}) e mostre no papel
o resultado esperado. Não relaxe os asserts existentes.
