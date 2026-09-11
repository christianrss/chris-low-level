using System.Runtime.InteropServices;

namespace Chris.PeLab;

public static class PeExportSpan
{
    /// <summary>validate MZ header and PE signature.</summary>
    public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        // PEDAGOGY-SOLUTION: DN-PE-EXP-01
        if (data.Length < 0x40) return false;
        if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;
        if (!TryGetPeOffset(data, out int off)) return false;
        if (off + 4 > data.Length) return false;
        return data[off] == (byte)'P' && data[off + 1] == (byte)'E';
    }

    /// <summary>read e_lfanew from DOS header.</summary>
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        // PEDAGOGY-SOLUTION: DN-PE-EXP-02
        peOffset = 0;
        if (data.Length < 0x40) return false;
        peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));
        return peOffset > 0 && peOffset + 4 <= data.Length;
    }

    /// <summary>read export directory RVA from optional header data dir [0].</summary>
    public static bool TryReadExportRva(ReadOnlySpan<byte> data, out uint exportRva)
    {
        // PEDAGOGY-SOLUTION: DN-PE-EXP-03
        exportRva = 0;
        if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;
        int opt = pe + 4 + 20;
        if (opt + 0x78 + 8 > data.Length) return false;
        exportRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78, 4));
        return true;
    }
}
