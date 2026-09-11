using System.Runtime.InteropServices;
namespace Chris.PeLab;
public static class PeImportSpan
{
    public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-01
        if (data.Length < 0x40) return false;
        if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;
        if (!TryGetPeOffset(data, out int off)) return false;
        if (off + 4 > data.Length) return false;
        return data[off] == (byte)'P' && data[off + 1] == (byte)'E';
    }
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-02
        peOffset = 0;
        if (data.Length < 0x40) return false;
        peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));
        return peOffset > 0 && peOffset + 4 <= data.Length;
    }
    public static bool TryReadImportRva(ReadOnlySpan<byte> data, out uint importRva)
    {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-03
        importRva = 0;
        if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;
        int opt = pe + 4 + 20; // optional header start
        // PE32+ magic 0x20B at opt+0; import dir is data directory[1] at opt+0x78+8
        if (opt + 0x78 + 16 > data.Length) return false;
        importRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78 + 8, 4));
        return true;
    }
}
