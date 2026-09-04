# Benchmarking methodology

A benchmark is an experiment. A number without methodology is weak evidence.

## Minimum protocol

1. State the question or hypothesis.
2. Record CPU, OS, compiler/interpreter and build flags.
3. Separate setup from the operation being measured where possible.
4. Warm up runtimes/caches when appropriate.
5. Run multiple repetitions.
6. Record median and, when useful, mean/min/max.
7. Keep benchmark inputs deterministic.
8. Compare against a baseline.
9. Interpret the result and list confounders.

Do not optimize only for a benchmark. Use profiling to connect the measured change to a plausible mechanism.
