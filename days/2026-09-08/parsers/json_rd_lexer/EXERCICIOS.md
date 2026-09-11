# Exercícios — json_rd_lexer

## Fácil — paper-trace do Caso 1

Reproduza no papel o trace numérico da `TEORIA_PASSO_A_PASSO.md` (mesmos bytes/estados do teste).
Arquivo-alvo: nenhum (caderno). Critério de aceite: os números batem com `TESTES_GUIADOS.md` Caso 1 **antes** de editar código.

## Médio — `PAR-JSON-LEX-01`

Implemente `skip_ws` em `starter/json_lex.c`.
Critério de aceite: o `PEDAGOGY-TEST` ligado a `PAR-JSON-LEX-01` PASS; valores iguais ao paper-trace.

## Difícil — `PAR-JSON-LEX-02` + `PAR-JSON-LEX-03`

Complete `next_token` e `lex_count` mantendo invariantes dos passos anteriores.
Critério de aceite: suíte completa do starter PASS; caso negativo (erro/bounds) ainda falha como documentado.

## Desafio — extensão sem quebrar testes

Altere apenas documentação ou um assert extra local: escolha um input *vizinho* ao Caso 1
(ex.: PUSH 256, 5º push no anel, id WASM 3, logits {1000,1001,1002}) e mostre no papel
o resultado esperado. Não relaxe os asserts existentes.
