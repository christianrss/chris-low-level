using System.Buffers;
using System.Buffers.Binary;

namespace Chris.DotNet.Buffers;

public readonly record struct FrameHeader(int PayloadLength, int MessageType);

public static class FrameCodec
{
    public const int HeaderSize = 8;

    public static void WriteHeader(Span<byte> destination, FrameHeader header)
    {
        if (destination.Length < HeaderSize)
            throw new ArgumentException("destination is smaller than frame header", nameof(destination));
        if (header.PayloadLength < 0)
            throw new ArgumentOutOfRangeException(nameof(header), "payload length cannot be negative");

        // TODO [D2-CSHARP-WRITE-HEADER]: write both Int32 fields in little-endian order.
        destination[..HeaderSize].Clear();
    }

    public static FrameHeader ReadHeader(ReadOnlySpan<byte> source)
    {
        if (source.Length < HeaderSize)
            throw new ArgumentException("source is smaller than frame header", nameof(source));

        // TODO [D2-CSHARP-READ-HEADER]: decode the two fields without allocating.
        var payloadLength = 0;
        var messageType = 0;
        if (payloadLength < 0)
            throw new InvalidDataException("encoded payload length is negative");
        return new FrameHeader(payloadLength, messageType);
    }

    public static PooledFrame RentFrame(ReadOnlySpan<byte> payload, int messageType)
    {
        // TODO [D2-CSHARP-RENT-FRAME]: rent, encode header, copy payload, transfer ownership.
        var required = checked(HeaderSize + payload.Length);
        var buffer = new byte[required];
        return new PooledFrame(buffer, required);
    }
}

public sealed class PooledFrame : IDisposable
{
    private byte[]? _buffer;
    public int Length { get; }

    internal PooledFrame(byte[] buffer, int length)
    {
        _buffer = buffer;
        Length = length;
    }

    public ReadOnlyMemory<byte> Memory => _buffer is null
        ? throw new ObjectDisposedException(nameof(PooledFrame))
        : _buffer.AsMemory(0, Length);

    public void Dispose()
    {
        var buffer = Interlocked.Exchange(ref _buffer, null);
        if (buffer is not null)
            ArrayPool<byte>.Shared.Return(buffer, clearArray: false);
    }
}
