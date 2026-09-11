# Exercícios — clvm_disassembler

## Fácil — paper-trace do Caso 1

Reproduza no papel o trace numérico da `TEORIA_PASSO_A_PASSO.md` (mesmos bytes/estados do teste).
Arquivo-alvo: nenhum (caderno). Critério de aceite: os números batem com `TESTES_GUIADOS.md` Caso 1 **antes** de editar código.

## Médio — `CLVM-DIS-01`

Implemente `decode_push` em `starter/clvm_disasm.c`.
Critério de aceite: o `PEDAGOGY-TEST` ligado a `CLVM-DIS-01` PASS; valores iguais ao paper-trace.

## Difícil — `CLVM-DIS-02` + `CLVM-DIS-03`

Complete `decode_branch` e `disassemble_all` mantendo invariantes dos passos anteriores.
Critério de aceite: suíte completa do starter PASS; caso negativo (erro/bounds) ainda falha como documentado.

## Desafio — extensão sem quebrar testes

Altere apenas documentação ou um assert extra local: escolha um input *vizinho* ao Caso 1
(ex.: PUSH 256, 5º push no anel, id WASM 3, logits {1000,1001,1002}) e mostre no papel
o resultado esperado. Não relaxe os asserts existentes.
