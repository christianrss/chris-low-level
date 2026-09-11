# Exercícios — ActivitySource e spans (.NET)

Cada nível mapeia aos TODOs `DN-ACT-SOURCE-01`, `DN-ACT-SPAN-02`, `DN-ACT-EXPORT-03`.

## Fácil

Escreva a string de export esperada.

**Arquivo-alvo:** `starter/ActivityLab.cs`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

CreateSource.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

StartWorkSpan + Export.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

O que Export devolve se act é null?

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
