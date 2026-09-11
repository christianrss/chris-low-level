# START HERE — Day 2026-09-10

**Integração multi-trilha — preparação capstone** (Dias 01–09 → 13 módulos).

## Fluxo por módulo

1. TEORIA → checkpoint em [`ATIVIDADES.md`](ATIVIDADES.md) → EXERCICIOS → starter → TESTES → RESOLUCAO (se travar).
2. Paper-trace **antes** do editor; o assert literal é a fonte de verdade.

## Ordem por bloco

1. `systems/clvm_pipeline_integration` + `rust/cross_verify_clvm`
2. `systems/unified_input_pipeline` + `linux/composite_input_driver` + `dotnet/capstone_input_host`
3. `graphics/pipeline_state_object` + `redteam/capstone_triage` + `quantum/capstone_measurement` + `ai/capstone_tokenizer`
4. `nodejs/capstone_stream_pipeline` + `parsers/capstone_query_eval` + `agent/capstone_agent_loop` + `tooling/capstone_format_detect`

## Capstones de portfólio

- `projects/chris-vm/` — CLVM + verify
- `projects/chris-driver-lab/` — input
- `projects/chris-binary-toolkit/` — triage
- `projects/chris-agent-harness/` — agent loop

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-10
python scripts/day_contract_check.py --day 2026-09-10
python scripts/run_day_tests.py --day 2026-09-10 --mode solutions
```

## Ordem cognitiva (não pule)

1. Leia o `README.md` do dia e marque as linguagens de cada módulo.
2. Abra `ATIVIDADES.md` e faça o checkpoint do Bloco 1 **no papel**.
3. Só então entre em `TEORIA_PASSO_A_PASSO.md` do primeiro módulo.
4. Implemente TODOs na ordem do mapa da RESOLUCAO; não leia `solutions/` antes.
5. Feche o bloco com o teste e volte ao checkpoint do próximo bloco.

## Comandos de validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-10
python scripts/run_day_tests.py --day 2026-09-10 --mode solutions
```

## Se travar

Use a seção **Onde colocar** da RESOLUCAO (arquivo + função + substituir). Se a seção não nomear o arquivo, o artefato está incompleto — reporte; não invente outro path.

