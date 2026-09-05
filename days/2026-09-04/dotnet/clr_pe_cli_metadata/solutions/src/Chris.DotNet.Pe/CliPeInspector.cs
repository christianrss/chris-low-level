using System.Buffers.Binary;

namespace Chris.DotNet.Pe;

public readonly record struct CliImageInfo(uint CliHeaderRva, uint CliHeaderSize, uint MetadataRva, uint MetadataSize, int MetadataFileOffset);

public static class CliPeInspector
{
    public static CliImageInfo Inspect(ReadOnlySpan<byte> image)
    {
        RequireRange(image, 0, 0x40);
        if (image[0] != (byte)'M' || image[1] != (byte)'Z') throw new InvalidDataException("missing MZ signature");
        var peOffset = checked((int)ReadU32(image, 0x3C));
        RequireRange(image, peOffset, 24);
        if (!image.Slice(peOffset, 4).SequenceEqual(new byte[] { (byte)'P', (byte)'E', 0, 0 })) throw new InvalidDataException("missing PE signature");

        var coff = peOffset + 4;
        var sectionCount = ReadU16(image, coff + 2);
        var optionalSize = ReadU16(image, coff + 16);
        var optional = coff + 20;
        RequireRange(image, optional, optionalSize);
        var magic = ReadU16(image, optional);
        var directoryStart = magic switch { 0x10B => optional + 96, 0x20B => optional + 112, _ => throw new InvalidDataException("unsupported PE optional-header magic") };
        const int cliDirectoryIndex = 14;
        var cliEntry = directoryStart + cliDirectoryIndex * 8;
        RequireRange(image, cliEntry, 8);
        var cliRva = ReadU32(image, cliEntry);
        var cliSize = ReadU32(image, cliEntry + 4);
        if (cliRva == 0 || cliSize < 16) throw new InvalidDataException("CLI header directory is missing");

        var sectionTable = optional + optionalSize;
        // PEDAGOGY-SOLUTION: D2-CLR-CLI-RVA
        var cliOffset = RvaToOffset(image, cliRva, sectionTable, sectionCount);
        RequireRange(image, cliOffset, 16);
        var metadataRva = ReadU32(image, cliOffset + 8);
        var metadataSize = ReadU32(image, cliOffset + 12);
        // PEDAGOGY-SOLUTION: D2-CLR-METADATA-RVA
        var metadataOffset = RvaToOffset(image, metadataRva, sectionTable, sectionCount);
        RequireRange(image, metadataOffset, 4);
        if (ReadU32(image, metadataOffset) != 0x424A5342) throw new InvalidDataException("metadata root does not start with BSJB");
        return new(cliRva, cliSize, metadataRva, metadataSize, metadataOffset);
    }

    private static int RvaToOffset(ReadOnlySpan<byte> image, uint rva, int sectionTable, int sectionCount)
    {
        for (var i = 0; i < sectionCount; ++i)
        {
            var section = sectionTable + i * 40;
            RequireRange(image, section, 40);
            var virtualSize = ReadU32(image, section + 8);
            var virtualAddress = ReadU32(image, section + 12);
            var rawSize = ReadU32(image, section + 16);
            var rawPointer = ReadU32(image, section + 20);
            var extent = Math.Max(virtualSize, rawSize);
            if (rva >= virtualAddress && (ulong)rva < (ulong)virtualAddress + extent)
                return checked((int)(rawPointer + (rva - virtualAddress)));
        }
        throw new InvalidDataException($"RVA 0x{rva:X8} does not map to any section");
    }

    private static ushort ReadU16(ReadOnlySpan<byte> image, int offset) { RequireRange(image, offset, 2); return BinaryPrimitives.ReadUInt16LittleEndian(image[offset..]); }
    private static uint ReadU32(ReadOnlySpan<byte> image, int offset) { RequireRange(image, offset, 4); return BinaryPrimitives.ReadUInt32LittleEndian(image[offset..]); }
    private static void RequireRange(ReadOnlySpan<byte> image, int offset, int length)
    {
        if (offset < 0 || length < 0 || offset > image.Length - length) throw new InvalidDataException("truncated PE/CLI image");
    }
}
