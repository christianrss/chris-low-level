# Exercícios — Driver composto de input

Cada nível mapeia aos TODOs `CAP-LNX-COMP-01`, `CAP-LNX-EVDEV-02`, `CAP-LNX-SYNC-03`.

## Fácil

Escreva SYN no papel.

**Arquivo-alvo:** `starter/composite_input_driver.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

device name.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

ev + frame SYN.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Dois SYN seguidos — o que significa?

**Critério:** resposta escrita no relatório + teste mental/extra sem quebrar os asserts oficiais.

## Extensão documentada (após os quatro níveis)

1. Adicione um caso negativo novo no papel (não no teste ainda): entrada malformada.
2. Preveja o retorno de erro (código, exceção, `Err`).
3. Só se o professor pedir: transforme a previsão em `PEDAGOGY-TEST` extra.

## Rubrica de aceite

| Nível | Aceite |
|-------|--------|
| Fácil | número do Caso 1 no caderno correto |
| Médio | implementação do TODO correspondente verde |
| Difícil | caso negativo + invariante citados |
| Desafio | extensão documentada com previsão de erro |
