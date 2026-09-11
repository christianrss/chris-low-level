# Exercícios — Amostra de stack e resolução de símbolos (Rust)

Cada nível mapeia aos TODOs `RS-STACK-SAMPLE-01`, `RS-STACK-FRAME-02`, `RS-STACK-REPORT-03`.

## Fácil

Anote no papel PC→nome do Caso 1.

**Arquivo-alvo:** `starter/src/lib.rs`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

Implemente resolve_frame.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

Monte o report com main.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

O que reportar se o PC não está no mapa?

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
