// PEDAGOGY-TEST [DN-SPAN-01]: parse stored deflate block header
// PEDAGOGY-TEST [DN-SPAN-02]: inflate stored deflate via Span<byte>
// PEDAGOGY-TEST [DN-SPAN-03]: validate LEN/NLEN complement
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `dotnet run` em starter/ — inflate de bloco stored.
// Caso 2: **Stored block:** BFINAL=1 BTYPE=00 + LEN/NLEN + payload.
// Caso 3: **Truncado:** buffer curto → InvalidDataException.
// Caso 4: **Span:** sem alocação extra além do array de saída.
// Caso 5: Valide solutions/ com os mesmos asserts.
using System.IO;

namespace Chris.IlLab;

static class DeflateStored
{
    public static int ReadStoredHeader(ReadOnlySpan<byte> input, out int dataOffset, out int length)
    {
        // TODO [DN-SPAN-01]
        throw new NotImplementedException("DN-SPAN-01");
    }

    public static byte[] InflateStored(ReadOnlySpan<byte> input)
    {
        // TODO [DN-SPAN-02]
        // TODO [DN-SPAN-03]
        throw new NotImplementedException("DN-SPAN-02");
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
        block[0] = 0x01; // BFINAL=1, BTYPE=00
        block[1] = (byte)(len & 0xFF);
        block[2] = (byte)(len >> 8);
        block[3] = (byte)(nlen & 0xFF);
        block[4] = (byte)(nlen >> 8);
        payload.CopyTo(block, 5);
        return block;
    }
}
