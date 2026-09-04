# Chris HTTP

## Problem
Parsing bytes incrementally is the foundation beneath a socket HTTP client/server.

## Current milestone
Incremental request parser with request line, headers and Content-Length body.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Build
```bash
cmake -S projects/chris-http -B build/chris-http
cmake --build build/chris-http --config Release
```

## Tests
```bash
ctest --test-dir build/chris-http --output-on-failure
```

## Benchmark
```bash
./build/chris-http/http_benchmark
```

Benchmarks are educational baselines. Record CPU, OS, compiler/runtime, warm-up strategy, repetitions and input size before comparing numbers.

## Next milestones
- case-insensitive header model
- limits/timeouts and parser hardening
- response parser
- TCP server on localhost
- keep-alive
- chunked transfer encoding
- connection pool and concurrency

## Limitations
This is not a production HTTP parser and deliberately implements only a small learning subset.

## Portfolio/research angle
Each milestone should add a regression test, a design note and a measurable experiment rather than only more features.
