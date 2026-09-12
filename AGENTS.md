# AGENTS.md — instruções para agentes de código

Este repositório usa **OpenSpec** + gates Python para evitar dias incompletos (ver lição Dia 07).

## Leitura obrigatória

1. [`openspec/README.md`](openspec/README.md) e [`openspec/specs/day-contract/spec.md`](openspec/specs/day-contract/spec.md)
2. [`docs/PROMPT_MESTRE_EXTREME_QUALITY.md`](docs/PROMPT_MESTRE_EXTREME_QUALITY.md)
3. [`docs/PEDAGOGY_STANDARD.md`](docs/PEDAGOGY_STANDARD.md)
4. Referências de qualidade legadas: [`days/2026-09-03/graphics/dual_backend_3d/`](days/2026-09-03/graphics/dual_backend_3d/) e [`days/2026-09-06/README.md`](days/2026-09-06/README.md)

## Antes de criar ou expandir um dia

1. Rodar **`/opsx:propose`** (OpenSpec) com tema, lane e ciclo — ou ler `openspec/changes/<slug>/proposal.md`
2. Para dias posteriores a 2026-09-11, usar `profile: depth_first`: exatamente 1 projeto, 6–8 h e starter quase vazio
3. Confirmar a rotação em `openspec/specs/day-contract/cycles/`; cobertura é por ciclo de 7–10 dias, não por matriz diária
4. Não usar `generate_day_scaffold.py` sem `--manifest-only` em dias já curados

## Gates finais (todos PASS antes de marcar done)

```powershell
python scripts/pedagogy_check_unified.py --day YYYY-MM-DD
python scripts/day_contract_check.py --day YYYY-MM-DD
python scripts/run_day_tests.py --day YYYY-MM-DD --mode starter --expect-fail
python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
python scripts/run_depth_mutants.py --day YYYY-MM-DD
python scripts/cycle_contract_check.py --cycle CYCLE_ID
```

`pedagogy_check` já inclui `day_contract_check` para o mesmo `--day`.

## Anti-padrões (Dia 07)

- PASS em `pedagogy_check` por módulo com dia **incompleto** (7–9 módulos vs 13 tier-A)
- Aplicar a matriz tier-A de 13 módulos a dias novos `depth_first`
- Starter com o núcleo já implementado ou microtarefas resolvíveis por retorno constante
- Teoria preenchida para atingir contagem de linhas, inclusive listas numeradas reescritas
- `README` / `ATIVIDADES` / `MANIFEST.modules` com contagens diferentes
- Plano narrow (ex. só GFX) sem atualizar `LEARNING_PATHS` e `module_project_map`
- `generate_day_scaffold` sobrescrevendo `START_HERE.md` curado com template genérico
- **GFX stub:** `solutions/**` Win32 com `MessageBox` como “demo” em vez de janela com pixels (ver [`docs/GFX_PEDAGOGY_STANDARD.md`](docs/GFX_PEDAGOGY_STANDARD.md) regra #8 e `openspec/specs/gfx-visual/spec.md`)

## Novo projeto depth-first

- Pacote canônico: 7 docs MD + `starter/` + `solutions/` (ver `PEDAGOGY_STANDARD.md`)
- Adicionar `day.contract.yaml`, `ASSESSMENT.yaml` e `RUBRIC.md`
- Declarar `student_owned`, 6–10 marcos, ≥10 comportamentos, ≥4 falhas e mutantes críticos
- Atualizar: `TODO_MAP.md`, `VALIDATION.md`, `docs/LEARNING_PATHS.md`, `scripts/module_project_map.py`
- Regenerar inventário: `python scripts/generate_day_scaffold.py --day YYYY-MM-DD --manifest-only`

## OpenSpec CLI (opcional)

```bash
npm install -g @fission-ai/openspec
openspec init --tools cursor
```

Sem CLI: use artefatos em `openspec/specs/` e `openspec/changes/` diretamente.
