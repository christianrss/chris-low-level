# AGENTS.md — instruções para agentes de código

Este repositório usa **OpenSpec** + gates Python para evitar dias incompletos (ver lição Dia 07).

## Leitura obrigatória

1. [`openspec/README.md`](openspec/README.md) e [`openspec/specs/day-contract/spec.md`](openspec/specs/day-contract/spec.md)
2. [`docs/PROMPT_MESTRE_EXTREME_QUALITY.md`](docs/PROMPT_MESTRE_EXTREME_QUALITY.md)
3. [`docs/PEDAGOGY_STANDARD.md`](docs/PEDAGOGY_STANDARD.md)
4. Dia referência multi-trilha: [`days/2026-09-06/README.md`](days/2026-09-06/README.md)

## Antes de criar ou expandir um dia

1. Rodar **`/opsx:propose`** (OpenSpec) com tema + dia referência — ou ler `openspec/changes/<slug>/proposal.md`
2. Confirmar `module_count` e **trilhas obrigatórias** em `openspec/specs/day-contract/tracks.yaml` antes de codar
3. Se o plano anexado omitir trilhas (red team, quantum, AI, Node, etc.), **expandir escopo** ou pedir ACK explícito ao usuário
4. Não usar `generate_day_scaffold.py` sem `--manifest-only` em dias já curados

## Gates finais (todos PASS antes de marcar done)

```powershell
python scripts/pedagogy_check_unified.py --day YYYY-MM-DD
python scripts/day_contract_check.py --day YYYY-MM-DD
python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
```

`pedagogy_check` já inclui `day_contract_check` para o mesmo `--day`.

## Anti-padrões (Dia 07)

- PASS em `pedagogy_check` por módulo com dia **incompleto** (7–9 módulos vs 13 tier-A)
- `README` / `ATIVIDADES` / `MANIFEST.modules` com contagens diferentes
- Plano narrow (ex. só GFX) sem atualizar `LEARNING_PATHS` e `module_project_map`
- `generate_day_scaffold` sobrescrevendo `START_HERE.md` curado com template genérico
- **GFX stub:** `solutions/**` Win32 com `MessageBox` como “demo” em vez de janela com pixels (ver [`docs/GFX_PEDAGOGY_STANDARD.md`](docs/GFX_PEDAGOGY_STANDARD.md) regra #8 e `openspec/specs/gfx-visual/spec.md`)

## Novo módulo em dia tier-A

- Pacote canônico: 7 docs MD + `starter/` + `solutions/` (ver `PEDAGOGY_STANDARD.md`)
- Atualizar: `TODO_MAP.md`, `VALIDATION.md`, `docs/LEARNING_PATHS.md`, `scripts/module_project_map.py`
- Regenerar inventário: `python scripts/generate_day_scaffold.py --day YYYY-MM-DD --manifest-only`

## OpenSpec CLI (opcional)

```bash
npm install -g @fission-ai/openspec
openspec init --tools cursor
```

Sem CLI: use artefatos em `openspec/specs/` e `openspec/changes/` diretamente.
