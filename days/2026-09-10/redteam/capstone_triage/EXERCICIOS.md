# Exercícios — Triage de magic bytes

Cada nível mapeia aos TODOs `CAP-RT-FMT-01`, `CAP-RT-FMT-02`, `CAP-RT-FMT-03`.

## Fácil

Magics ELF/PE/WASM no papel.

**Arquivo-alvo:** `starter/capstone_triage.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

detect_magic.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

min_size + triage.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Mach-O magic?

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
