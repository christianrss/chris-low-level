# Exercícios — Tokenizer + merge de runs

Cada nível mapeia aos TODOs `CAP-AI-TOK-01`, `CAP-AI-TOK-02`, `CAP-AI-TOK-03`.

## Fácil

ord de aaab.

**Arquivo-alvo:** `starter/capstone_tokenizer.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

ids.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

merge + vocab.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

BPE um passo de merge.

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
