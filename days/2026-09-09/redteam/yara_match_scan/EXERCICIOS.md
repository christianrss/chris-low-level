# Exercícios — Scan estilo YARA (Python)

Cada nível mapeia aos TODOs `RT-YARA-PARSE-01`, `RT-YARA-MATCH-02`, `RT-YARA-TRIAGE-03`.

## Fácil

Parse AA ?? no papel.

**Arquivo-alvo:** `starter/yara_scan.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

match_at.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

scan_all.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Suporte a nibble wildcard A?.

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
