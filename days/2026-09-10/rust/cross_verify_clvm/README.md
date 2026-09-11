# Cross-verify header CLVM (Rust)

**Dia:** 2026-09-10 · **Trilha:** `rust` · **Módulo:** `cross_verify_clvm`  
**Linguagem:** Rust  
**TODOs:** `CAP-RS-XVFY-01`, `CAP-RS-XVFY-02`, `CAP-RS-XVFY-03`

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

Valida magic `CLVM`, version 1 e FNV no offset 12 — o mesmo contrato do loader C, em Rust memory-safe.
