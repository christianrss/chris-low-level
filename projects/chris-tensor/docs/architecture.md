# Architecture

`Tensor2D` owns contiguous row-major storage. `TensorView2D` stores a pointer plus row/column strides, allowing the transpose to be represented without copying. `matmul` consumes views so future kernels can reason about arbitrary layouts.
