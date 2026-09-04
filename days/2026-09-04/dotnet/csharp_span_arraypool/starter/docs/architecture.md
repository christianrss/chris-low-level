# Architecture
`FrameCodec` is stateless. It writes fixed-width little-endian headers into caller-owned spans. `RentFrame` rents the backing byte array from the shared pool and returns explicit lifetime ownership through `PooledFrame : IDisposable`.

The design deliberately separates **buffer ownership** from **buffer view**. `Span<T>`/`ReadOnlySpan<T>` are temporary views; `PooledFrame` owns the rented array and is responsible for returning it exactly once.
