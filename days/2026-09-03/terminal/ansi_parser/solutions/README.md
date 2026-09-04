# Chris Terminal

## Problem
Terminal emulators are protocol state machines: byte streams change cursor, grid and mode state.

## Current milestone
Portable text-grid + incremental ESC/CSI parser for a small ECMA-48 subset.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-terminal -B build/chris-terminal
cmake --build build/chris-terminal --config Release
```

## Tests
```bash
ctest --test-dir build/chris-terminal --output-on-failure
```

## Benchmark
```bash
./build/chris-terminal/terminal_benchmark
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- multiple CSI parameters
- SGR attributes/colors
- UTF-8 decoder
- scrollback and alternate screen
- PTY/ConPTY integration
- mouse reporting and resizing
- remote SSH-backed session

## Limitations
No PTY, UTF-8, terminal modes or full ECMA-48 compatibility yet.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
