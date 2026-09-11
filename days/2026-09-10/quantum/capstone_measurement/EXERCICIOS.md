# Exercícios — Medição Born e amostragem

Cada nível mapeia aos TODOs `CAP-Q-MEAS-01`, `CAP-Q-MEAS-02`, `CAP-Q-MEAS-03`.

## Fácil

Calcule |0.5+0.5j|^2.

**Arquivo-alvo:** `starter/capstone_measurement.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

born_probability.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

measure_sample.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Amostragem com RNG real vs limiar fixo.

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
