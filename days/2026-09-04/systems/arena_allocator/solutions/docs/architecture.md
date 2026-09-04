# Architecture

`Arena` owns one byte buffer and a monotonically increasing offset. Allocation computes the aligned absolute address, converts it back to an offset and advances the cursor. `reset()` discards all allocations together by setting the cursor to zero.

The implementation deliberately exposes alignment and lifetime trade-offs before more sophisticated allocators are introduced.
