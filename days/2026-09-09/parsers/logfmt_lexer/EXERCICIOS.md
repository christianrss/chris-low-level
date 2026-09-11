# Exercícios — Lexer logfmt (Python)

Cada nível mapeia aos TODOs `PR-LOGFMT-LEX-01`, `PR-LOGFMT-KV-02`, `PR-LOGFMT-ESC-03`.

## Fácil

Tokenize a=1 b=2 no papel.

**Arquivo-alvo:** `starter/logfmt.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

tokenize + parse_kv.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

escapes.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Como tratar aspas "a=b c=d"?

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
