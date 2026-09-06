// PEDAGOGY-TEST [DN-SPAN-01]: parse stored deflate block header
// PEDAGOGY-TEST [DN-SPAN-02]: inflate stored deflate via Span<byte>
// PEDAGOGY-TEST [DN-SPAN-03]: validate LEN/NLEN complement
// PEDAGOGY-SOLUTION: DN-SPAN-01
// PEDAGOGY-SOLUTION: DN-SPAN-02
// PEDAGOGY-SOLUTION: DN-SPAN-03
using System.IO;

namespace Chris.IlLab;

static class DeflateStored
{
    public static int ReadStoredHeader(ReadOnlySpan<byte> input, out int dataOffset, out int length)
    {
        if (input.Length < 5)
        {
            throw new InvalidDataException("truncated stored header");
        }

        byte header = input[0];
        if (((header >> 1) & 0x03) != 0x00)
        {
            throw new InvalidDataException("not stored block");
        }

        ushort len = (ushort)(input[1] | (input[2] << 8));
        ushort nlen = (ushort)(input[3] | (input[4] << 8));
        if ((ushort)(len ^ nlen) != 0xFFFF)
        {
            throw new InvalidDataException("len/nlen mismatch");
        }

        dataOffset = 5;
        length = len;
        return dataOffset;
    }

    public static byte[] InflateStored(ReadOnlySpan<byte> input)
    {
        int offset = ReadStoredHeader(input, out int dataOffset, out int length);
        if (input.Length < dataOffset + length)
        {
            throw new InvalidDataException("truncated stored payload");
        }

        var output = new byte[length];
        input.Slice(dataOffset, length).CopyTo(output);
        return output;
    }
}

static class Program
{
    static void Main()
    {
        byte[] payload = "LOWLEVEL"u8.ToArray();
        byte[] block = BuildStoredBlock(payload);

        var inflated = DeflateStored.InflateStored(block);
        if (!inflated.AsSpan().SequenceEqual(payload))
        {
            throw new Exception("inflate mismatch");
        }

        try
        {
            DeflateStored.InflateStored(block.AsSpan(0, 3));
            throw new Exception("truncated accepted");
        }
        catch (InvalidDataException)
        {
        }

        Console.WriteLine("OK deflate stored");
    }

    static byte[] BuildStoredBlock(byte[] payload)
    {
        ushort len = (ushort)payload.Length;
        ushort nlen = (ushort)~len;
        var block = new byte[1 + 2 + 2 + payload.Length];
        block[0] = 0x01;
        block[1] = (byte)(len & 0xFF);
        block[2] = (byte)(len >> 8);
        block[3] = (byte)(nlen & 0xFF);
        block[4] = (byte)(nlen >> 8);
        payload.CopyTo(block, 5);
        return block;
    }
}
