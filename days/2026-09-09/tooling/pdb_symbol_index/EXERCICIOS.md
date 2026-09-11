# Exercícios — Índice de símbolos estilo PDB (Python)

Cada nível mapeia aos TODOs `TL-PDB-PARSE-01`, `TL-PDB-INDEX-02`, `TL-PDB-LOOKUP-03`.

## Fácil

Parse 1000 main no papel.

**Arquivo-alvo:** `starter/pdb_index.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

parse_symbol_line.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

index + lookup.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Suporte a linha com demangle?

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
