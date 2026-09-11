# Exercícios — GPU timer query (simulação headless)

Cada nível mapeia aos TODOs `GFX-GPU-TIMER-01`, `GFX-GPU-LAP-02`, `GFX-GPU-BENCH-03`.

## Fácil

Qual o primeiro handle?

**Arquivo-alvo:** `starter/gpu_timer.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

begin_query.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

end_query + lap_times.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Dois begins aninhados: quantos handles?

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
