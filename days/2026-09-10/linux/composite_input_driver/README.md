# Driver composto de input

**Dia:** 2026-09-10 · **Trilha:** `linux` · **Módulo:** `composite_input_driver`  
**Linguagem:** Python  
**TODOs:** `CAP-LNX-COMP-01`, `CAP-LNX-EVDEV-02`, `CAP-LNX-SYNC-03`

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

Um device virtual `composite0` agrega evdev e fecha o frame com SYN `(0,0,0)`.
