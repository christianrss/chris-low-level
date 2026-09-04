# Chris Algorithms

## Problem
Algorithm study should connect proofs and asymptotic analysis with the behavior of real implementations on real inputs.

## Current milestone
Instrumented merge sort and quicksort with correctness tests and reproducible input distributions.

## Day 02 research question
How do input distribution and pivot policy change comparison counts and observed runtime even when asymptotic notation looks similar?

## Important limitation
The current quicksort intentionally uses the last element as pivot so sorted/reversed inputs expose a bad case. This is a teaching baseline, not a production sorter.

## Next milestones
Median-of-three/randomized pivots, introspective fallback, branch/cache profiling, radix sort, selection algorithms and a reusable benchmark harness.
