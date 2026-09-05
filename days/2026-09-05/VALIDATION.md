# VALIDATION — Day 03 (2026-09-05)

Data: 2026-09-05

## Gates executados

| Gate | Resultado | Detalhe |
|------|-----------|---------|
| `pedagogy_check_unified.py --day 2026-09-05` | **PASS** | 10 módulos, 23 TODOs |
| TEORIA ≥ 120 linhas + diagramas | **PASS** | 10/10 (128–134 linhas) |
| EXERCICIOS.md | **PASS** | 10/10 |
| RESOLUCAO ≥ 80 linhas + Relatório | **PASS** | 10/10 |
| BENCHMARK `## Resultados observados` | **PASS** | 10/10 |
| PEDAGOGY-TEST markers | **PASS** | em testes starter |
| Bug AnsiParser | **CORRIGIDO** | starter usa `AnsiParser` consistente com testes |
| `backpressure_demo.js` | **INTEGRADO** | `starter/test.js` exige demo |

## Comandos de validação

```bash
python scripts/pedagogy_check_unified.py --day 2026-09-05
python scripts/run_day_tests.py --day 2026-09-05 --mode solutions
python scripts/run_day_tests.py --day 2026-09-05 --mode starter --expect-fail
python scripts/build_day_docx.py --day 2026-09-05
```

## Execução disponível

- Python 3.13, GCC/G++ 14.2, CMake 3.31, Node 22.
- Solutions portáteis: pkg, bitmap, matmul, ELF, streams, VM, graphics states, ANSI.
- Starters: falham nos TODOs planejados (não por API quebrada).

## Indisponível / não alegado

- SDK .NET: CIL validado estruturalmente; executar localmente com `dotnet run`.
- Kernel module real: `chris_char.c` é revisão de fonte; modelo userspace é o artefato executado.
- Vulkan/D3D12/GPU real: simulador de estados + shaders fonte; sem backend GPU.
- `glslangValidator` / `dxc`: shaders não compilados neste ambiente.

## Formato de estudo

**Principal:** Markdown modular — cada pasta `<trilha>/<modulo>/` contém teoria, exercícios, resolução guiada e código (`starter/` + `solutions/`). Comece pelo `START_HERE.md` do dia.

**Opcional:** `Treino_LowLevel_Unificado_YYYY-MM-DD.docx` — export gerado por `scripts/build_day_docx.py` (não é a fonte primária).

## Artefatos do dia

- `START_HERE.md`, `TODO_MAP.md`, `MANIFEST.json`, `VALIDATION.md`
- `Treino_LowLevel_Unificado_2026-09-05.docx` — export opcional via `build_day_docx.py`

## Nota sobre `days/2026-09-05-v2/`

Pasta **deprecated** — ver `DEPRECATED.md`. Entrega canônica é esta pasta.
