using System.Buffers;
using System.Buffers.Binary;

namespace Chris.DotNet.Buffers;

public readonly record struct FrameHeader(int PayloadLength, int MessageType);

public static class FrameCodec
{
    public const int HeaderSize = 8;

    // PEDAGOGY-SOLUTION: D2-CSHARP-WRITE-HEADER
public static void WriteHeader(Span<byte> destination, FrameHeader header)
    {
        if (destination.Length < HeaderSize)
            throw new ArgumentException("destination is smaller than frame header", nameof(destination));
        if (header.PayloadLength < 0)
            throw new ArgumentOutOfRangeException(nameof(header), "payload length cannot be negative");

        BinaryPrimitives.WriteInt32LittleEndian(destination[0..4], header.PayloadLength);
        BinaryPrimitives.WriteInt32LittleEndian(destination[4..8], header.MessageType);
    }

    // PEDAGOGY-SOLUTION: D2-CSHARP-READ-HEADER
public static FrameHeader ReadHeader(ReadOnlySpan<byte> source)
    {
        if (source.Length < HeaderSize)
            throw new ArgumentException("source is smaller than frame header", nameof(source));

        var payloadLength = BinaryPrimitives.ReadInt32LittleEndian(source[0..4]);
        var messageType = BinaryPrimitives.ReadInt32LittleEndian(source[4..8]);
        if (payloadLength < 0)
            throw new InvalidDataException("encoded payload length is negative");
        return new FrameHeader(payloadLength, messageType);
    }

    // PEDAGOGY-SOLUTION: D2-CSHARP-RENT-FRAME
public static PooledFrame RentFrame(ReadOnlySpan<byte> payload, int messageType)
    {
        var required = checked(HeaderSize + payload.Length);
        var buffer = ArrayPool<byte>.Shared.Rent(required);
        WriteHeader(buffer.AsSpan(0, HeaderSize), new FrameHeader(payload.Length, messageType));
        payload.CopyTo(buffer.AsSpan(HeaderSize, payload.Length));
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
