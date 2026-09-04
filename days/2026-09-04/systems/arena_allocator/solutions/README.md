# Chris Arena

## Problem
General-purpose heap allocation is convenient but can hide metadata, synchronization and fragmentation costs. An arena makes lifetime and alignment explicit.

## Current milestone
A fixed-capacity bump allocator with power-of-two alignment, exhaustion checks and O(1) bulk reset.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build and test
```bash
cmake -S projects/chris-arena -B build/chris-arena -DCMAKE_BUILD_TYPE=Release
cmake --build build/chris-arena --config Release
ctest --test-dir build/chris-arena --output-on-failure
```

## Benchmark
Enable `CHRIS_BUILD_BENCHMARKS=ON` and compare arena allocation with individually owned heap blocks. Treat the result as a machine-specific experiment, not a universal claim.

## Limitations
The allocator cannot free individual objects, is not thread-safe and does not run destructors automatically.

## Next milestones
Markers/rewind, typed helpers, debug poisoning, guard regions, per-thread arenas and slab-size-class comparison.
