# json_rd_lexer

**Trilha:** `parsers` · **Dia:** 2026-09-08

## O que você constrói

Implementação low-level com TODOs `PAR-JSON-LEX-01`, `PAR-JSON-LEX-02`, `PAR-JSON-LEX-03`. Leia a TEORIA (trace numérico) antes do starter.

## Pré-requisitos

Módulos do Dia 03/07 na mesma trilha quando houver continuação (CLVM, input, PE).

## Como rodar

```powershell
cd days/2026-09-08/parsers/json_rd_lexer/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

Starter: FAIL até completar TODOs. Solutions: PASS.

## Ordem de estudo

1. `TEORIA_PASSO_A_PASSO.md`
2. Checkpoint em `../../ATIVIDADES.md`
3. `EXERCICIOS.md` → código em `starter/`
4. `TESTES_GUIADOS.md` / `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` se travar
5. `BENCHMARK_GUIADO.md` + Relatório
