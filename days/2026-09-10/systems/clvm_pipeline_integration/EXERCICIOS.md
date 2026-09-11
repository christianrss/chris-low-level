# Exercícios — Pipeline CLVM: disasm + peephole + verify

Cada nível mapeia aos TODOs `CAP-CLVM-DIS-01`, `CAP-CLVM-PEEP-02`, `CAP-CLVM-VFY-03`.

## Fácil

Disasm no papel do fixture PUSH1 PUSH2 ADD HALT.

**Arquivo-alvo:** `starter/clvm_pipeline_integration.py`  
**Critério:** o paper-trace bate com o Caso 1 de `TESTES_GUIADOS.md` antes de compilar.

## Médio

disasm.

**Critério:** o primeiro `PEDAGOGY-TEST` passa.

## Difícil

peephole + verify.

**Critério:** todos os testes do módulo PASS no starter completo.

## Desafio

Peephole PUSH 0 SUB?

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
