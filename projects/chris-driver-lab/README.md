# Chris Driver Lab

## Problem
Real NIC/storage/GPU drivers exchange work with devices through descriptor queues and ownership rules. A simulator lets those invariants be learned safely before MMIO/DMA.

## Current milestone
Portable descriptor-ring ownership simulator.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-driver-lab -B build/chris-driver-lab
cmake --build build/chris-driver-lab --config Release
```

## Tests
```bash
ctest --test-dir build/chris-driver-lab --output-on-failure
```

## Benchmark
```bash
./build/chris-driver-lab/driver_ring_benchmark
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- model RX and TX separately
- interrupt vs polling simulation
- MMIO register model
- virtio descriptor structure
- QEMU virtio-net driver
- PCI enumeration and MSI-X

## Limitations
No MMIO, DMA, interrupts or real hardware access. This is deliberately a state-machine model.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
