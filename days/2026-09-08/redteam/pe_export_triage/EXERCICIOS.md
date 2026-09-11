# Exercícios — pe_export_triage

## Fácil — paper-trace do Caso 1

Reproduza no papel o trace numérico da `TEORIA_PASSO_A_PASSO.md` (mesmos bytes/estados do teste).
Arquivo-alvo: nenhum (caderno). Critério de aceite: os números batem com `TESTES_GUIADOS.md` Caso 1 **antes** de editar código.

## Médio — `RT-PE-EXP-01`

Implemente `validate_mz_pe` em `starter/pe_export_triage.py`.
Critério de aceite: o `PEDAGOGY-TEST` ligado a `RT-PE-EXP-01` PASS; valores iguais ao paper-trace.

## Difícil — `RT-PE-EXP-02` + `RT-PE-EXP-03`

Complete `count_export_names` e `flag_suspicious_exports` mantendo invariantes dos passos anteriores.
Critério de aceite: suíte completa do starter PASS; caso negativo (erro/bounds) ainda falha como documentado.

## Desafio — extensão sem quebrar testes

Altere apenas documentação ou um assert extra local: escolha um input *vizinho* ao Caso 1
(ex.: PUSH 256, 5º push no anel, id WASM 3, logits {1000,1001,1002}) e mostre no papel
o resultado esperado. Não relaxe os asserts existentes.
