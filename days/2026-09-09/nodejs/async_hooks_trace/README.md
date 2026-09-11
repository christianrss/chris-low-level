# async_hooks: fases e métricas (JavaScript)

**Dia:** 2026-09-09 · **Trilha:** `nodejs` · **Módulo:** `async_hooks_trace`  
**Linguagem:** JavaScript  
**TODOs:** `ND-ASYNC-HOOK-01`, `ND-ASYNC-TIMELINE-02`, `ND-ASYNC-METRICS-03`

## Pré-requisitos

- Paper-trace da TEORIA (seção 4) feito no caderno
- Checkpoint correspondente em `ATIVIDADES.md` do dia

## Fluxo

1. `TEORIA_PASSO_A_PASSO.md`
2. `EXERCICIOS.md`
3. Implemente `starter/`
4. `TESTES_GUIADOS.md` / teste local
5. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só se travar
6. `BENCHMARK_GUIADO.md`

## Ideia em uma frase

O event loop cria recursos async. `async_hooks` observa init/before/after. O lab grava eventos, formata timeline e conta fases.
