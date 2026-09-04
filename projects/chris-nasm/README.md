# Chris NASM

## Problem
A real assembler removes the mystery between textual Assembly and exact instruction bytes.

## Current milestone
Python learning assembler that emits correct x86-64 bytes for `nop`, `ret`, `int3`, `syscall`, `mov r64, imm64` (first eight GPRs) and `db`.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-nasm -B build/chris-nasm
```

## Tests
```bash
ctest --test-dir build/chris-nasm --output-on-failure
```

## Benchmark
```bash
python projects/chris-nasm/benchmarks/benchmark.py
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- tokenizer and expression grammar
- labels and two-pass symbol resolution
- ModR/M and SIB addressing
- prefixes/opcode tables
- sections/directives/macros
- ELF64 relocatable object writer
- COFF writer
- linker integration

## Limitations
This is intentionally a tiny subset, not a NASM replacement. No labels, ModR/M, object files or macros yet.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
