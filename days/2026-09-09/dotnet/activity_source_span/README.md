# ActivitySource e spans (.NET)

**Dia:** 2026-09-09 · **Trilha:** `dotnet` · **Módulo:** `activity_source_span`  
**Linguagem:** C#  
**TODOs:** `DN-ACT-SOURCE-01`, `DN-ACT-SPAN-02`, `DN-ACT-EXPORT-03`

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

OpenTelemetry/.NET Diagnostics usam ActivitySource para criar spans. O lab fixa nome da source, tag `module`, e export textual `op|tag`.
