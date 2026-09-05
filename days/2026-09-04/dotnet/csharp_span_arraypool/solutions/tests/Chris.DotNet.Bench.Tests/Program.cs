// PEDAGOGY-TEST: D2-CSHARP-WRITE-HEADER
// PEDAGOGY-TEST: D2-CSHARP-READ-HEADER
// PEDAGOGY-TEST: D2-CSHARP-RENT-FRAME
using Chris.DotNet.Buffers;

static void Require(bool condition, string message)
{
    if (!condition) throw new Exception(message);
}

Span<byte> headerBytes = stackalloc byte[FrameCodec.HeaderSize];
FrameCodec.WriteHeader(headerBytes, new FrameHeader(1234, 7));
var decoded = FrameCodec.ReadHeader(headerBytes);
Require(decoded == new FrameHeader(1234, 7), "header round-trip failed");

var payload = new byte[] { 1, 2, 3, 4 };
using (var frame = FrameCodec.RentFrame(payload, 99))
{
    var memory = frame.Memory.Span;
    Require(FrameCodec.ReadHeader(memory[..8]) == new FrameHeader(4, 99), "rented header mismatch");
    Require(memory[8..12].SequenceEqual(payload), "payload mismatch");
}

var disposed = FrameCodec.RentFrame(payload, 77);
disposed.Dispose();
bool disposedAccessRejected = false;
try { _ = disposed.Memory; }
catch (ObjectDisposedException) { disposedAccessRejected = true; }
Require(disposedAccessRejected, "Memory after Dispose must fail");

bool shortBufferRejected = false;
try { FrameCodec.WriteHeader(stackalloc byte[4], new FrameHeader(1, 1)); }
catch (ArgumentException) { shortBufferRejected = true; }
Require(shortBufferRejected, "short destination must be rejected");
Console.WriteLine("chris-dotnet-bench tests passed");
