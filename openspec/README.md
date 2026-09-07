# OpenSpec — governança de mudanças

Este diretório segue o layout [OpenSpec](https://openspec.dev/) para alinhar agentes e humanos **antes** de codar.

## Instalação (opcional, para slash commands no Cursor)

```bash
npm install -g @fission-ai/openspec
openspec init --tools cursor
```

Se o CLI não estiver instalado, use os artefatos em `specs/` e `changes/` diretamente.

## Workflow

1. **`/opsx:propose`** (ou ler `changes/<slug>/proposal.md`) — escopo, dia referência, trilhas
2. Revisar `specs/` + delta no change
3. **`/opsx:apply`** — implementar tasks
4. Gates obrigatórios:
   ```powershell
   python scripts/pedagogy_check_unified.py --day YYYY-MM-DD
   python scripts/day_contract_check.py --day YYYY-MM-DD
   python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
   ```
5. **`/opsx:archive`** — mover change para `changes/archive/`

## Specs (fonte da verdade)

| Spec | Conteúdo |
|------|----------|
| [specs/day-layout/](specs/day-layout/spec.md) | Layout `days/YYYY-MM-DD/` |
| [specs/day-contract/](specs/day-contract/spec.md) | Completude multi-trilha + infra |
| [specs/pedagogy/](specs/pedagogy/spec.md) | Thresholds pedagógicos |
| [specs/learning-paths/](specs/learning-paths/spec.md) | Trilhas verticais |

Ver também [AGENTS.md](../AGENTS.md) na raiz do repositório.
