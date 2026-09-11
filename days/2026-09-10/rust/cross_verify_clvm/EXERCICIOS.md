# Exercícios — Cross-verify header CLVM (Rust)

Cada nível mapeia aos TODOs `CAP-RS-XVFY-01`, `CAP-RS-XVFY-02`, `CAP-RS-XVFY-03`.

## Fácil

Tabela de offsets no papel.

**Arquivo-alvo:** `starter/src/lib.rs`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

magic+version.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

FNV @12.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

flags != 0 deve falhar?

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
