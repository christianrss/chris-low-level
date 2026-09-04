# Low-Level Unified Engineering Lab

A long-term learning and research portfolio focused on building systems from first principles.

The repository combines three mandatory tracks every day:

1. **Systems / Low-Level Engineering** - runtimes, VMs, operating systems, browsers, databases, emulators, graphics, compilers, debuggers and performance.
2. **AI / ML Systems Low-Level** - manual gradients, autograd, tensor runtimes, CPU/GPU kernels, inference, training, quantization and serving.
3. **Safe Red Team / Reverse Engineering** - benign binaries only, assembly, PE/ELF, debugging and defensive binary tooling.

Extra tracks rotate through graphics, physics, animation, multimedia, storage, browser engines and virtualization.

## Repository model

```text
days/YYYY-MM-DD/   -> complete pedagogical material for that day
projects/          -> cumulative, portfolio-quality projects
benchmarks/        -> reproducible measurements and small results
research/          -> hypotheses, experiment notes, results and conclusions
docs/              -> methodology, architecture, testing and environment notes
scripts/           -> repository automation
.github/workflows/ -> CI
```

The `days/` tree intentionally contains `starter/` and `solutions/`. The `projects/` tree does not: it is the clean software that evolves over time.

## Active projects after Day 01

| Project | Area | Current milestone |
|---|---|---|
| `chris-vm` | Systems | CLVM bytecode loader + stack VM + branches |
| `chris-autograd` | AI systems | manual linear training + scalar autograd |
| `chris-disassembler` | Binary tooling | ELF/PE inspection + first x86-64 decoder |
| `chris-binary-toolkit` | Safe RE | benign target + ASCII string extractor |
| `chris-renderer` | Graphics | shared math/physics + software/OpenGL Windows backends |

## Quick start

Read [`START_HERE.md`](START_HERE.md), then open the Day 01 DOCX under `days/2026-09-03/`.

Portable validation from the repository root:

```bash
python scripts/quality_check.py
python scripts/run_all_tests.py
python scripts/run_all_benchmarks.py
```

On Windows, use a Visual Studio Developer PowerShell or a terminal with CMake available.

## Portfolio principles

Every project should eventually demonstrate:

- clear problem statement and architecture;
- reproducible build;
- unit/integration/regression tests;
- benchmarks with a stated methodology;
- profiling when optimization begins;
- honest limitations and trade-offs;
- experiment notes and measured conclusions;
- meaningful Git history rather than code dumps.

The goal is not to imitate production systems feature-for-feature. The goal is to understand and implement the mechanisms that make those systems work.
