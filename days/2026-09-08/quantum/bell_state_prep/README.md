# bell_state_prep

**Trilha:** `quantum` · **Dia:** 2026-09-08

## O que você constrói

Implementação low-level com TODOs `Q-BELL-01`, `Q-BELL-02`, `Q-BELL-03`. Leia a TEORIA (trace numérico) antes do starter.

## Pré-requisitos

Módulos do Dia 03/07 na mesma trilha quando houver continuação (CLVM, input, PE).

## Como rodar

```powershell
cd days/2026-09-08/quantum/bell_state_prep/starter
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
