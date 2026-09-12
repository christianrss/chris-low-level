# Baseline dos gates legados

Capturado em 2026-09-12 durante a introdução do perfil depth-first.
Este documento registra dívida preexistente; não autoriza reescrever os
dias legados.

## Day contract

- `2026-09-03`: FAIL — README é interpretado como “1 módulo”, mas há 13.
- `2026-09-04`: FAIL — `MANIFEST.modules=11`, filesystem com 12.
- `2026-09-05` a `2026-09-11`: PASS.

## Pedagogy all-days

O conteúdo de 2026-09-03 a 2026-09-11 foi detectado com 13, 12, 10,
13, 21, 22, 24, 23 e 23 módulos, respectivamente. O gate termina em
FAIL somente pelos dois erros de contrato acima.

## Solution tests de referência

- `2026-09-03`: 13/13 módulos PASS.
- `2026-09-06`: 13/13 módulos PASS.

Esses dois dias cobrem o código de referência curado e o antigo modelo
multi-trilha, incluindo CMake, Python, Node.js, Rust e .NET.

## Quality check

O gate global já falha por linhas longas em geradores legados como
`bootstrap_v2_pedagogy.py`, `deepen_*`, `repair_*` e `rewrite_*`.
Esses arquivos estão congelados como geradores de conteúdo legado em
`scripts/LEGACY_CONTENT_GENERATORS.md`.

## Política de comparação

Mudanças depth-first não podem adicionar uma nova falha a esta lista.
Correções da dívida legada exigem escopo próprio. O CI depth-first usa
fixtures independentes e não converte essas falhas históricas em PASS.
