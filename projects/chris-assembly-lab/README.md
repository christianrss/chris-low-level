# Chris Assembly Lab

## Problem
Hand-written Assembly exposes ABI contracts, registers, memory addressing and arithmetic at the machine boundary.

## Current milestone
Linux x86-64 System V function that sums an array and is called from C.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-assembly-lab -B build/chris-assembly-lab
cmake --build build/chris-assembly-lab --config Release
```

## Tests
```bash
ctest --test-dir build/chris-assembly-lab --output-on-failure
```

## Benchmark
```bash
./build/chris-assembly-lab/assembly_benchmark
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- Windows x64 MASM version
- ARM64 version
- RISC-V version
- syscall-only program
- SIMD sum and profiling
- atomics and memory-ordering labs

## Limitations
Current executable target is Linux x86-64 System V only. The benchmark compares source implementations, not necessarily equivalent compiler vectorization.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
