# Exercícios — Profiler de opcodes CLVM (C)

Cada nível mapeia aos TODOs `CLVM-TRACE-01`, `CLVM-TRACE-02`, `CLVM-TRACE-03`.

## Fácil

No papel: conte `02 02 08` → c[2], c[8], hottest.

**Arquivo-alvo:** `starter/trace.c`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

Implemente `note_op` e rode só o assert de c[2]==2.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

Implemente `hottest` + `profile_code`.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Se todos counts forem 0, hottest devolve 0. Explique por quê isso é aceitável neste lab.

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
