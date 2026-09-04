# chris-autograd

A from-scratch path from scalar gradient descent to a small tensor/autograd runtime.

Day 01 contains two independent views of learning:

- manual analytical gradients for `y = w*x + b` in Python and C;
- a scalar computation graph with reverse-mode automatic differentiation.

## Test strategy

- convergence test for the known line `y=2x+1`;
- numerical gradient check against central differences;
- gradient accumulation when a node is reused;
- negative test for unsupported operations.

## Benchmark direction

Day 01 records a Python/C scalar baseline. Future milestones will move from scalar work to contiguous tensor storage, strides, vectorization, GEMM, threading and GPU kernels.

## Research direction

A useful early experiment is numerical stability of finite-difference gradient checking versus epsilon and floating-point precision.

## Build and test

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
python benchmarks/benchmark.py
```

## Limitations

The current autograd engine is scalar, has a deliberately tiny operation set and does not yet model tensors, devices, broadcasting or graph lifetime concerns.

## Next milestones

1. contiguous tensor storage and shape metadata;
2. strides and indexing;
3. elementwise kernels;
4. broadcasting rules;
5. matrix multiplication baseline;
6. SIMD/threaded kernels and profiler-backed optimization.
