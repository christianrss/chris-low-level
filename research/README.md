# Research notebook

This directory stores cross-project experiments. Project-specific hypotheses stay under each `projects/<name>/research/` directory.

## Day 01 research habits

- gradient-checking epsilon sweep;
- VM dispatch-overhead decomposition;
- decoder validation corpus and byte-for-byte assembler comparisons;
- binary-scanner throughput scaling;
- software vs GPU rendering methodology;
- C vs Assembly microbenchmark methodology and why hand-written Assembly can lose;
- toy CPU dispatch cost and instruction-mix experiments;
- terminal parser throughput vs input fragmentation;
- HTTP parser throughput vs header/body size and chunk fragmentation;
- gossip reachability/duplicate delivery under topology and TTL changes;
- toy PoW cost as difficulty changes;
- descriptor-ring capacity/wraparound/throughput studies.

## Standard experiment shape

1. State a falsifiable question or hypothesis.
2. Freeze a baseline and environment.
3. Change one controlled variable when possible.
4. Run enough repetitions to expose noise.
5. Preserve small raw/summary results.
6. Explain confounders and limitations.
7. Add a regression test when the experiment reveals a correctness bug.
8. Write the conclusion even when the hypothesis was wrong.
