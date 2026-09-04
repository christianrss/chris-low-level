# Chris Chain

## Problem
A local toy chain exposes hash linking, Merkle aggregation, proof-of-work search and tamper detection without interacting with real-money networks.

## Current milestone
Deterministic local hash-chain + Merkle root + toy proof-of-work.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-chain -B build/chris-chain
```

## Tests
```bash
ctest --test-dir build/chris-chain --output-on-failure
```

## Benchmark
```bash
python projects/chris-chain/benchmarks/benchmark.py
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- transaction serialization model
- UTXO model
- mempool
- fork/reorg simulation
- peer propagation with chris-p2p
- wallet using audited signature library
- local node RPC/explorer
- consensus/failure experiments

## Limitations
No real economic security, signatures, networking or production consensus. Never use this code for money or key custody.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
