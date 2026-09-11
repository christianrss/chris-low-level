using System.Runtime.InteropServices;
namespace Chris.PeLab;
public static class PeImportSpan
{
    /// <summary>TODO [DOTNET-IMP-01]: validate MZ + PE signature via Span.</summary>
    public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        _ = data; return false;
    }
    /// <summary>TODO [DOTNET-IMP-02]: read e_lfanew (offset 0x3C).</summary>
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        peOffset = 0; _ = data; return false;
    }
    /// <summary>TODO [DOTNET-IMP-03]: read import directory RVA (data dir[1]) from PE32+ optional header.</summary>
    public static bool TryReadImportRva(ReadOnlySpan<byte> data, out uint importRva)
    {
        importRva = 0; _ = data; return false;
    }
}
