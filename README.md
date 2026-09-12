# Low-Level Unified Engineering & Research Portfolio

A long-term repository for learning computer systems from first principles while producing software, measurements and research notes that can become a serious engineering portfolio.

The target is not to collect tutorial projects. The target is to build **vertical understanding**: from logic gates, ISA encodings and firmware to kernels, drivers, protocols, compilers, emulators, graphics and ML systems.

## Depth-first curriculum

Days through 2026-09-11 are a legacy catalogue. Every later day contains
**one authentic 6–8 hour project**, with a near-empty starter and a
measurable end-to-end result. Breadth is achieved by rotating curriculum
lanes across a 7–10 day cycle, not by repeating every track every day.

The lanes are systems, architecture, operating systems, networking,
graphics, AI systems, safe reverse engineering, runtimes, quantum and
tooling. A project has one primary lane but may integrate several
languages where the problem naturally requires them.

## Permanent advanced tracks

- CPU architecture: x86-64, ARM64 and RISC-V.
- Bootloaders, BIOS/UEFI, firmware and platform initialization.
- Assemblers, linkers, loaders and debug formats.
- Kernels, filesystems and device drivers.
- Terminals, shells, SSH, cryptography and network protocols.
- P2P, distributed systems, blockchain and toy cryptocurrencies.
- Emulation, virtualization, JIT/DBT and hypervisor concepts.
- Graphics, software rasterization, GPU concepts, physics and multimedia.
- Browser, database, storage and distributed systems internals.
- Projects that normally feel "magical": allocators, runtimes, profilers, containers, Git-like storage, TCP/IP stacks and more.

## Repository model

```text
days/YYYY-MM-DD/   complete pedagogical material for that day
projects/          cumulative portfolio-quality implementations
benchmarks/        reproducible measurements + small result files
research/          hypotheses, experiments, ablations and conclusions
docs/              methodology, architecture, safety and reading maps
scripts/           validation, benchmarks, porting map, depth upgrades
.github/workflows/ CI
```

`days/` intentionally contains `starter/` and `solutions/`. `projects/` contains the clean cumulative software that should look like normal engineering repositories.

## Day 01 implemented projects

| Project | Current milestone | Tests |
|---|---|---|
| `chris-vm` | CLVM binary format + stack VM | integration |
| `chris-autograd` | manual linear training + scalar autograd | gradient/regression |
| `chris-disassembler` | ELF/PE inspection + first x86-64 decoding | integration |
| `chris-binary-toolkit` | benign binary/string tooling | unit |
| `chris-renderer` | shared 3D/physics core + software/OpenGL Win32 backends | unit |
| `chris-lantern-hunt` | FPS horror OpenGL: procgen, normal maps, miniaudio, spotlight | unit (procgen/collision) |
| `chris-assembly-lab` | System V x86-64 ABI function in Assembly | unit + benchmark |
| `chris-cpu` | tiny fetch/decode/execute CPU | unit + benchmark |
| `chris-nasm` | real x86-64 encoding for a tiny instruction subset | byte-for-byte unit tests |
| `chris-boot` | 512-byte legacy BIOS boot-sector byte model + NASM source | binary layout tests |
| `chris-terminal` | ECMA-48/ANSI terminal-state parser subset | golden/state tests |
| `chris-http` | incremental HTTP/1.x request parser | fragmentation/negative tests |
| `chris-p2p` | deterministic in-process gossip simulator | topology/property tests |
| `chris-chain` | local toy blockchain/hash-chain laboratory | tamper/PoW/Merkle tests |
| `chris-driver-lab` | NIC descriptor-ring simulator | wrap/full/order tests |

## Portfolio standard

Every mature project should eventually show:

- a precise problem statement;
- architecture and ADRs;
- reproducible build;
- unit/integration/regression/property/fuzz tests as appropriate;
- benchmarks with methodology and raw small results;
- profiling when performance work begins;
- limitations and trade-offs;
- specification references;
- experiments and measured conclusions;
- useful Git history and releases;
- eventually, contributions upstream or external users.

## Start

Read [`START_HERE.md`](START_HERE.md), then open the day folder you are studying:

The entries below are the **legacy collection**, preserved as published.
They are useful references, but their module counts are not templates
for future days.

| Day | Path | Modules | Benchmarks |
|-----|------|---------|------------|
| 2026-09-03 | [`days/2026-09-03/`](days/2026-09-03/) | 13 | [`benchmarks/results-2026-09-03.json`](benchmarks/results-2026-09-03.json) |
| 2026-09-04 | [`days/2026-09-04/`](days/2026-09-04/) | 11 | [`benchmarks/results-2026-09-04.json`](benchmarks/results-2026-09-04.json) |
| 2026-09-05 | [`days/2026-09-05/`](days/2026-09-05/) | 10 | [`benchmarks/results-2026-09-05.json`](benchmarks/results-2026-09-05.json) |
| 2026-09-06 | [`days/2026-09-06/`](days/2026-09-06/) | 13 (compressão + portal Verlet + Rust) | — |
| 2026-09-07 | [`days/2026-09-07/`](days/2026-09-07/) | 21 (CLVM v2 + input + multi-trilha) | [`benchmarks/results-2026-09-07.json`](benchmarks/results-2026-09-07.json) |
| 2026-09-08 | [`days/2026-09-08/`](days/2026-09-08/) | 13 (CLVM toolchain + input mux) | — |
| 2026-09-09 | [`days/2026-09-09/`](days/2026-09-09/) | 13 (observabilidade + profiling) | — |
| 2026-09-10 | [`days/2026-09-10/`](days/2026-09-10/) | 13 (integração capstone) | — |
| 2026-09-11 | [`days/2026-09-11/`](days/2026-09-11/) | 23 (reloc/ABI + labs incorporados) | — |

Published depth-first days (one project, 6–8 h):

| Day | Path | Project | Capstone |
|-----|------|---------|----------|
| 2026-09-12 | [`days/2026-09-12/`](days/2026-09-12/) | `systems/clvm_xdbg` | `projects/chris-debugger` |

### Fluxo por projeto depth-first

```text
day.contract.yaml + ASSESSMENT.yaml
  → baseline e previsão de falhas
  → teoria + traces + invariantes
  → testes de fronteira
  → starter/                  (construir o núcleo)
  → caminho mínimo end-to-end
  → robustez + mutantes críticos
  → benchmark + RUBRIC.md
  → solutions/                (comparação tardia)
  → projects/chris-*          (porte cumulativo)
```

Cada projeto contém 7 documentos canônicos + `starter/` + `solutions/`.
**Markdown é o formato principal**; DOCX é export opcional.

### Documentação pedagógica

| Doc | Conteúdo |
|-----|----------|
| [`docs/PEDAGOGY_STANDARD.md`](docs/PEDAGOGY_STANDARD.md) | O quê / Como / Por quê; artefatos obrigatórios |
| [`docs/PORTING_GUIDE.md`](docs/PORTING_GUIDE.md) | Como portar lab → `projects/` |
| [`docs/LEARNING_PATHS.md`](docs/LEARNING_PATHS.md) | Trilhas verticais multi-dia + capstones |
| [`docs/RESEARCH_NOTE_TEMPLATE.md`](docs/RESEARCH_NOTE_TEMPLATE.md) | Template para experimentos em `research/` |
| [`docs/PROMPT_MESTRE_TREINO_LOW_LEVEL.md`](docs/PROMPT_MESTRE_TREINO_LOW_LEVEL.md) | Índice do prompt mestre |
| [`docs/PROMPT_MESTRE_EXTREME_QUALITY.md`](docs/PROMPT_MESTRE_EXTREME_QUALITY.md) | Thresholds e anti-padrões |
| [`AGENTS.md`](AGENTS.md) | Instruções para agentes + OpenSpec |
| [`openspec/README.md`](openspec/README.md) | Spec-driven workflow (`/opsx:propose`) |

### Validação

```bash
# Novos dias depth-first
python scripts/day_contract_check.py --day YYYY-MM-DD
python scripts/pedagogy_check_unified.py --day YYYY-MM-DD
python scripts/run_day_tests.py --day YYYY-MM-DD --mode starter --expect-fail
python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
python scripts/run_depth_mutants.py --day YYYY-MM-DD
python scripts/cycle_contract_check.py --cycle CYCLE_ID

# Gate pedagógico + contrato de dia (módulos, trilhas, infra)
python scripts/pedagogy_check_unified.py --day 2026-09-03 --all-days
python scripts/day_contract_check.py --day 2026-09-06
python scripts/day_contract_check.py --day 2026-09-07
python scripts/day_contract_check.py --day 2026-09-08
python scripts/day_contract_check.py --day 2026-09-09
python scripts/day_contract_check.py --day 2026-09-10

# Testes dos módulos do dia (solutions devem passar)
python scripts/run_day_tests.py --day 2026-09-03 --mode solutions
python scripts/run_day_tests.py --day 2026-09-04 --mode solutions
python scripts/run_day_tests.py --day 2026-09-05 --mode solutions
python scripts/run_day_tests.py --day 2026-09-06 --mode solutions
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions
python scripts/run_day_tests.py --day 2026-09-09 --mode solutions
python scripts/run_day_tests.py --day 2026-09-10 --mode solutions

# Benchmarks → benchmarks/results-YYYY-MM-DD.json
python scripts/run_day_benchmarks.py --day 2026-09-03
python scripts/run_day_benchmarks.py --day 2026-09-04
python scripts/run_day_benchmarks.py --day 2026-09-05

# Projetos cumulativos
python scripts/quality_check.py
python scripts/run_all_tests.py
python scripts/run_all_benchmarks.py
```

Trilhas de execução real (kernel `insmod`, QEMU boot, .NET SDK):

```bash
python scripts/run_real_env_checklist.py --module linux/kernel_module_driver_lab --day 2026-09-05
```

Manutenção do acervo (após mudanças estruturais):

```bash
python scripts/upgrade_depth_e2e.py --all-days
python scripts/repair_pedagogy_depth.py
python scripts/generate_day_scaffold.py --day YYYY-MM-DD
```

Export DOCX opcional (não é gate de qualidade):

```bash
python scripts/build_day_docx.py --day 2026-09-03
python scripts/build_day_docx.py --day 2026-09-04
python scripts/build_day_docx.py --day 2026-09-05
```

CI (`.github/workflows/ci.yml`) roda pedagogy check + `run_day_tests --mode solutions` nos dias 03–06 + testes dos `projects/`.

The lab is intentionally honest about what was and was not tested. Hardware-specific, Windows-specific, firmware and QEMU milestones are documented separately until the required environment is available.

For the complete mapping from the user-defined curriculum directives to Day 01 evidence and future milestones, see [`docs/DIRECTIVES_COVERAGE.md`](docs/DIRECTIVES_COVERAGE.md).

## Day 06 — 2026-09-06

13 módulos: trilha compressão (RLE → Huffman → LZ77 → DEFLATE → zlib/gzip → PNG IDAT), `graphics/verlet_rope_3d`, tensor entropy, blob triage, Span deflate, gunzip transform e dois espelhos Rust. Capstone: `projects/chris-compress`. Extra: `projects/chris-lantern-hunt` (fora do dia). Ver [`days/2026-09-06/README.md`](days/2026-09-06/README.md).

## Day 05 — 2026-09-05

10 módulos: tiled matmul, CIL/.NET, estados GPU, VM bytecode com branches, rootfs/pkg, driver kernel (userspace + review), terminal ANSI, streams Node, ELF entry, bitmap page allocator. Projetos: `chris-tensor/day03_tiled_matmul`, `chris-dotnet-ilvm`, `chris-gpu-state`, `chris-js/day03_branches`, `chris-linux-pkg`, `chris-linux-module-lab`, `chris-linux-terminal`, `chris-node-streaming/day03_backpressure`, `chris-pagealloc`. Ver [`days/2026-09-05/README.md`](days/2026-09-05/README.md) e [`days/2026-09-05/START_HERE.md`](days/2026-09-05/START_HERE.md).

## Day 02 — 2026-09-04

Adds `chris-arena`, `chris-tensor`, `chris-algorithms` (**blocked merge**), `chris-qsim`, host-reference `chris-os` (**dirty-rect compositor**), `chris-debugger` protocol, ELF64 **Phdr/Shdr/dynsym** in `chris-binary-toolkit`, plus managed tracks `chris-dotnet-bench`, `chris-dotnet-pe`, `chris-node-streaming` and `chris-js`. See `days/2026-09-04/README.md`.
