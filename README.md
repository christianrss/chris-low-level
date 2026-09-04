# Low-Level Unified Engineering & Research Portfolio

A long-term repository for learning computer systems from first principles while producing software, measurements and research notes that can become a serious engineering portfolio.

The target is not to collect tutorial projects. The target is to build **vertical understanding**: from logic gates, ISA encodings and firmware to kernels, drivers, protocols, compilers, emulators, graphics and ML systems.

## Daily mandatory cores

1. **Systems / Low-Level Engineering** - C, C++, Rust, Python, Assembly, runtimes, toolchains, operating systems, storage, networks, emulation and performance.
2. **AI / ML Systems Low-Level** - manual gradients, autograd, tensor storage, kernels, SIMD, GPU, inference, training, quantization and serving.
3. **Safe Red Team / Reverse Engineering** - benign binaries and owned lab systems only; assembly, PE/ELF, debugging, deobfuscation, instrumentation and defensive telemetry.

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
days/YYYY-MM-DD/   complete pedagogical source/material for that day
projects/          cumulative portfolio-quality implementations
benchmarks/        reproducible measurements + small result files
research/          hypotheses, experiments, ablations and conclusions
docs/              methodology, architecture, safety and reading maps
scripts/           validation/build/benchmark automation
.github/workflows/ CI
```

`days/` intentionally contains `starter/` and `solutions/`. `projects/` contains the clean cumulative software that should look like normal engineering repositories.

The **master DOCX and package manifest are distributed in the daily ZIP**, not versioned in Git. This keeps binary/document-package churn out of the source history while preserving the full study artifact in each delivery.

## Day 01 implemented projects

| Project | Current milestone | Tests |
|---|---|---|
| `chris-vm` | CLVM binary format + stack VM | integration |
| `chris-autograd` | manual linear training + scalar autograd | gradient/regression |
| `chris-disassembler` | ELF/PE inspection + first x86-64 decoding | integration |
| `chris-binary-toolkit` | benign binary/string tooling | unit |
| `chris-renderer` | shared 3D/physics core + software/OpenGL Win32 backends | unit |
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

Read [`START_HERE.md`](START_HERE.md), then follow the Day 01 material under [`days/2026-09-03/`](days/2026-09-03/). The matching master DOCX is inside the daily ZIP delivery.

Portable repository validation:

```bash
python scripts/quality_check.py
python scripts/run_all_tests.py
python scripts/run_all_benchmarks.py
```

The lab is intentionally honest about what was and was not tested. Hardware-specific, Windows-specific, firmware and QEMU milestones are documented separately until the required environment is available.

For the complete mapping from the curriculum directives to Day 01 evidence and future milestones, see [`docs/DIRECTIVES_COVERAGE.md`](docs/DIRECTIVES_COVERAGE.md).
