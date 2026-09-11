# Exercícios — Pipeline unificado de input

Cada nível mapeia aos TODOs `CAP-INP-KBD-01`, `CAP-INP-MUX-02`, `CAP-INP-XFM-03`.

## Fácil

Anote (1,30,1) → KEY:30.

**Arquivo-alvo:** `starter/unified_input_pipeline.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

kbd path.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

mux + transform.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Ordenação temporal no mux.

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
