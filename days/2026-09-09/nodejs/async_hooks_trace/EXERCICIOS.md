# Exercícios — async_hooks: fases e métricas (JavaScript)

Cada nível mapeia aos TODOs `ND-ASYNC-HOOK-01`, `ND-ASYNC-TIMELINE-02`, `ND-ASYNC-METRICS-03`.

## Fácil

Liste as três fases no papel.

**Arquivo-alvo:** `starter/async_trace.js`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

installHooks.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

timeline + metrics.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

O que muda se usar setTimeout em vez de Promise?

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
