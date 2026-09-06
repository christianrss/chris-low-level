# Chris Algorithms

## Problem
Sorting that only fits in RAM is the CS101 case. Systems work cares about **tiling**: runs that fit in L1/L2 or in a disk page, then merge passes whose cost is dominated by block I/O.

## Current milestone
Blocked / external-style merge sort with `SortIoStats{comparisons, block_reads, block_writes}`.

## Day 02 research question
How do `tile_size` and the number of merge passes trade CPU comparisons against simulated tile loads/stores — and when does that beat a cache-oblivious in-memory quicksort narrative?

## Important limitation
I/O is **simulated** by counting tile-sized loads/stores over an in-memory vector. There is no real disk. The model teaches external-merge structure, not filesystem APIs.

## Next milestones
True k-way heap merge, double buffering, NUMA-aware tiling, radix for fixed-width keys, PMU cache-miss study vs tile size.
