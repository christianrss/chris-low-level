using System;
using Chris.PeLab;
using Xunit;
public class PeImportTests
{
    static byte[] MinimalPe()
    {
        var buf = new byte[0x200];
        buf[0] = (byte)'M'; buf[1] = (byte)'Z';
        BitConverter.GetBytes(0x80).CopyTo(buf, 0x3C);
        buf[0x80] = (byte)'P'; buf[0x81] = (byte)'E';
        BitConverter.GetBytes((ushort)0x20B).CopyTo(buf, 0x98); // pe+24 = optional magic
        // pe=0x80; opt=0x80+24=0x98; data dir[1] at opt+0x80 = 0x118? 
        // Day08 export used opt+0x78 for dir[0]. dir[1] = opt+0x78+8.
        // opt = pe+4+20 = 0x98. dir0 @ 0x98+0x78=0x110, dir1 @ 0x118
        BitConverter.GetBytes(0x2000u).CopyTo(buf, 0x118);
        return buf;
    }
    // PEDAGOGY-TEST: DOTNET-IMP-01
    [Fact] public void Caso1_IsPe() => Assert.True(PeImportSpan.IsPeFile(MinimalPe()));
    // PEDAGOGY-TEST: DOTNET-IMP-02
    [Fact] public void Caso2_Offset() {
        Assert.True(PeImportSpan.TryGetPeOffset(MinimalPe(), out int off));
        Assert.Equal(0x80, off);
    }
    // PEDAGOGY-TEST: DOTNET-IMP-03
    [Fact] public void Caso3_ImportRva() {
        Assert.True(PeImportSpan.TryReadImportRva(MinimalPe(), out uint rva));
        Assert.Equal(0x2000u, rva);
    }
}
