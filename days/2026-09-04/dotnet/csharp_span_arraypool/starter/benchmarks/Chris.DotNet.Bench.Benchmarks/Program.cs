using System.Diagnostics;
using Chris.DotNet.Buffers;

const int iterations = 500_000;
var payload = new byte[128];
for (var i = 0; i < 20_000; ++i) { using var warm = FrameCodec.RentFrame(payload, 1); }
GC.Collect(); GC.WaitForPendingFinalizers(); GC.Collect();
var before = GC.GetAllocatedBytesForCurrentThread();
var sw = Stopwatch.StartNew();
for (var i = 0; i < iterations; ++i)
{
    using var frame = FrameCodec.RentFrame(payload, i & 7);
    _ = frame.Memory.Span[0];
}
sw.Stop();
var allocated = GC.GetAllocatedBytesForCurrentThread() - before;
Console.WriteLine($"iterations={iterations} elapsed_ms={sw.Elapsed.TotalMilliseconds:F3} managed_alloc_bytes={allocated}");
Console.WriteLine("Interpret allocation carefully: PooledFrame itself is a managed object in this milestone.");
