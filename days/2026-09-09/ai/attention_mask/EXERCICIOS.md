# Exercícios — Máscara causal de atenção (C)

Cada nível mapeia aos TODOs `AI-ATTN-01`, `AI-ATTN-02`, `AI-ATTN-03`.

## Fácil

Tabela q=2 para k=0..3 no papel.

**Arquivo-alvo:** `starter/attn.c`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

Implemente causal_mask.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

apply_mask + visible_count.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Como mascarar uma matriz N×N com estas funções? Escreva o nested loop.

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
