# Chris CPU

## Problem
A tiny deterministic CPU makes fetch/decode/execute, instruction encoding, registers, memory and control flow concrete.

## Current milestone
16-bit educational CPU with four registers, byte-addressed memory and a small ISA.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-cpu -B build/chris-cpu
cmake --build build/chris-cpu --config Release
```

## Tests
```bash
ctest --test-dir build/chris-cpu --output-on-failure
```

## Benchmark
```bash
./build/chris-cpu/cpu_benchmark
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- flags and conditional branches
- stack/CALL/RET
- interrupt model
- pipeline simulator
- RISC-V decoder comparison

## Limitations
This is not a real ISA and does not model timing, caches, privilege or interrupts yet.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
