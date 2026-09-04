# Chris Tensor

## Problem
Tensor libraries hide shape, strides and memory layout. This project exposes those details before introducing vectorization or GPU kernels.

## Current milestone
Contiguous 2D float tensors, explicit strided views, zero-copy transpose views and a naïve matrix multiplication kernel.

## Research angle
The next experiments compare loop orders, transposed access, blocking/tiling and SIMD. The point is to connect arithmetic intensity with cache behavior rather than only report wall-clock time.

## Build/test
```bash
cmake -S projects/chris-tensor -B build/chris-tensor -DCMAKE_BUILD_TYPE=Release
cmake --build build/chris-tensor --config Release
ctest --test-dir build/chris-tensor --output-on-failure
```

## Limitations
Only rank-2 float tensors exist. There is no autograd, broadcasting, SIMD, threading or GPU backend yet.
