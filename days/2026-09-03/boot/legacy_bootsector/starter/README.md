# Chris Boot

## Problem
Boot code makes the CPU reset/firmware/kernel boundary visible.

## Current milestone
A 512-byte legacy BIOS image builder plus equivalent NASM source. Structural tests verify the boot signature and exact first instructions without committing generated binaries.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-boot -B build/chris-boot
```

## Tests
```bash
ctest --test-dir build/chris-boot --output-on-failure
```

## Benchmark
```bash
Not benchmarked: correctness and boot-state understanding matter more than throughput at this milestone.
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- run under QEMU/Bochs when available
- BIOS teletype loop/string output
- read sectors
- FAT12/16 loader
- A20/GDT/protected mode
- long-mode transition
- ELF64 kernel loader
- parallel UEFI application path

## Limitations
The NASM/QEMU path is not executed in the current Linux container because those tools are not installed. The Python builder emits a known minimal BIOS boot-sector byte sequence and is fully tested.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
