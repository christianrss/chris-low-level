# Pipeline CLVM: disasm + peephole + verify

**Dia:** 2026-09-10 · **Trilha:** `systems` · **Módulo:** `clvm_pipeline_integration`  
**Linguagem:** Python  
**TODOs:** `CAP-CLVM-DIS-01`, `CAP-CLVM-PEEP-02`, `CAP-CLVM-VFY-03`

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

Capstone systems: junta disassembler, peephole `PUSH 0; ADD`→noop, e verificação de stack no mesmo bytecode.
