# Exercícios — Duplex stream pipeline

Cada nível mapeia aos TODOs `CAP-ND-PIPE-01`, `CAP-ND-PIPE-03`, `CAP-ND-PIPE-02`.

## Fácil

Anote HELLO e chunks=1.

**Arquivo-alvo:** `starter/capstone_stream_pipeline.js`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

transform básico.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

metrics + flush.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Backpressure: o que pause faz?

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
