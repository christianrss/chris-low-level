# Exercícios — Verify + replay log FSM (Python)

Cada nível mapeia aos TODOs `AG-VERIFY-LOG-01`, `AG-REPLAY-FSM-02`, `AG-TRACE-HASH-03`.

## Fácil

Desenhe a FSM no papel.

**Arquivo-alvo:** `starter/agent_log.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

append_log.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

replay_fsm + hash.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

O que acontece com dois verify consecutivos?

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
