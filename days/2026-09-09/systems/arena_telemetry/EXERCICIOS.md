# Exercícios — Telemetria de arena bump (C++)

Cada nível mapeia aos TODOs `ARENA-TEL-01`, `ARENA-TEL-02`, `ARENA-TEL-03`.

## Fácil

Trace no papel: used após alloc(8) e após reset.

**Arquivo-alvo:** `starter/arena.cpp`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

Implemente init + alloc.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

Implemente reset sem apagar allocs.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

O que acontece se alloc(0)? Defina e documente (este lab não exige).

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
