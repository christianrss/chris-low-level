# Telemetria de arena bump (C++)

**Dia:** 2026-09-09 · **Trilha:** `systems` · **Módulo:** `arena_telemetry`  
**Linguagem:** C++  
**TODOs:** `ARENA-TEL-01`, `ARENA-TEL-02`, `ARENA-TEL-03`

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

A arena do Dia 04 só faz bump. Aqui cada alloc incrementa `allocs` e cada reset incrementa `resets`, mas reset **não** zera `allocs` — a métrica de vida útil sobrevive ao reuso do buffer.
