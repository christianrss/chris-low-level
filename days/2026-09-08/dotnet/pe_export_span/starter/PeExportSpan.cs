using System.Runtime.InteropServices;

namespace Chris.PeLab;

public static class PeExportSpan
{
    /// <summary>TODO [DN-PE-EXP-01]: validate MZ header and PE signature.</summary>
    public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        _ = data;
        return false;
    }

    /// <summary>TODO [DN-PE-EXP-02]: read e_lfanew from DOS header.</summary>
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        peOffset = 0;
        _ = data;
        return false;
    }

    /// <summary>TODO [DN-PE-EXP-03]: read export directory RVA from optional header data dir [0].</summary>
    public static bool TryReadExportRva(ReadOnlySpan<byte> data, out uint exportRva)
    {
        exportRva = 0;
        _ = data;
        return false;
    }
}
