# Máscara causal de atenção (C)

**Dia:** 2026-09-09 · **Trilha:** `ai` · **Módulo:** `attention_mask`  
**Linguagem:** C  
**TODOs:** `AI-ATTN-01`, `AI-ATTN-02`, `AI-ATTN-03`

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

Atenção causal impede o token de olhar o futuro. Com query index q, a key k só é visível se k≤q. Scores invisíveis viram −1e9 antes do softmax.
