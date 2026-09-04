# Architecture

Sorting functions operate in place and return `SortStats`. Keeping instrumentation explicit makes algorithmic cost observable without mixing timing logic into the implementation.
