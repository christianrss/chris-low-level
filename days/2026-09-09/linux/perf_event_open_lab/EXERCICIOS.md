# Exercícios — perf_event_open (simulação Python)

Cada nível mapeia aos TODOs `LX-PERF-OPEN-01`, `LX-PERF-READ-02`, `LX-PERF-CLOSE-03`.

## Fácil

Calcule fd de open(1,2) no papel.

**Arquivo-alvo:** `starter/perf_lab.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

Implemente open.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

read + close.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Como simular EBADF se read após close?

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
