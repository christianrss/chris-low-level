# perf_event_open (simulação Python)

**Dia:** 2026-09-09 · **Trilha:** `linux` · **Módulo:** `perf_event_open_lab`  
**Linguagem:** Python  
**TODOs:** `LX-PERF-OPEN-01`, `LX-PERF-READ-02`, `LX-PERF-CLOSE-03`

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

No Linux, `perf_event_open` devolve um fd de contador. Este lab simula open/read/close com fd sintético `(type<<16)|config` e um dict de contadores.
