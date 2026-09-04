# Chris P2P

## Problem
P2P systems replace a central request path with discovery, propagation, duplication control and failure handling.

## Current milestone
Deterministic in-process gossip simulator with TTL and duplicate suppression.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-p2p -B build/chris-p2p
```

## Tests
```bash
ctest --test-dir build/chris-p2p --output-on-failure
```

## Benchmark
```bash
python projects/chris-p2p/benchmarks/benchmark.py
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- latency/drop simulation
- peer scoring and backpressure
- bootstrap/discovery
- Kademlia-like routing table
- content chunks + hashes
- swarming download
- real localhost sockets
- NAT traversal concepts

## Limitations
No sockets, adversarial peers, NAT, cryptographic identity or DHT yet.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
