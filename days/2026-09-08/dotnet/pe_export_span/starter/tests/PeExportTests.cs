using System;
using System.Runtime.InteropServices;
using Chris.PeLab;
using Xunit;

public class PeExportTests
{
    static byte[] MinimalPe()
    {
        var buf = new byte[0x200];
        buf[0] = (byte)'M'; buf[1] = (byte)'Z';
        BitConverter.GetBytes(0x80).CopyTo(buf, 0x3C);
        buf[0x80] = (byte)'P'; buf[0x81] = (byte)'E'; buf[0x82] = 0; buf[0x83] = 0;
        BitConverter.GetBytes(0x20B).CopyTo(buf, 0x98);
        BitConverter.GetBytes(0x1000u).CopyTo(buf, 0x110);
        return buf;
    }

    // PEDAGOGY-TEST: DN-PE-EXP-01
// Test cases (TESTES_GUIADOS.md):
// Caso 1: IsPeFile
// Caso 2: pe offset
// Caso 3: export RVA
// Caso 4: not PE
    [Fact]
    public void Caso1_IsPeFile() => Assert.True(PeExportSpan.IsPeFile(MinimalPe()));

    // PEDAGOGY-TEST: DN-PE-EXP-02
    [Fact]
    public void Caso2_PeOffset()
    {
        Assert.True(PeExportSpan.TryGetPeOffset(MinimalPe(), out int off));
        Assert.Equal(0x80, off);
    }

    // PEDAGOGY-TEST: DN-PE-EXP-03
    [Fact]
    public void Caso3_ExportRva()
    {
        Assert.True(PeExportSpan.TryReadExportRva(MinimalPe(), out uint rva));
        Assert.Equal(0x1000u, rva);
    }

    // PEDAGOGY-TEST: DN-PE-EXP-01
    [Fact]
    public void Caso4_NotPe() => Assert.False(PeExportSpan.IsPeFile(new byte[] { 0, 1, 2 }));
}
