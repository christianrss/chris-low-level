# Verify + replay log FSM (Python)

**Dia:** 2026-09-09 · **Trilha:** `agent` · **Módulo:** `verify_replay_log`  
**Linguagem:** Python  
**TODOs:** `AG-VERIFY-LOG-01`, `AG-REPLAY-FSM-02`, `AG-TRACE-HASH-03`

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

Agentes registram eventos; replay deve reproduzir o estado. O lab faz append estruturado, FSM IDLE→RUN→DONE/REVISE e hash curto do log.
