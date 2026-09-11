# Exercícios — Canal de decoerência (Python)

Cada nível mapeia aos TODOs `Q-DECO-CHANNEL-01`, `Q-DECO-APPLY-02`, `Q-DECO-TRACE-03`.

## Fácil

Normalize um par (0.3,0.7) no papel.

**Arquivo-alvo:** `starter/decoherence.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

canal + soma 1.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

apply + trace len 4.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Escreva um canal que fixa ponto (0.5,0.5).

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
