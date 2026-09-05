// PEDAGOGY-TEST: D2-CLR-CLI-RVA
// PEDAGOGY-TEST: D2-CLR-METADATA-RVA
using System.Buffers.Binary;
using Chris.DotNet.Pe;

static void U16(Span<byte> b, int o, ushort v) => BinaryPrimitives.WriteUInt16LittleEndian(b[o..], v);
static void U32(Span<byte> b, int o, uint v) => BinaryPrimitives.WriteUInt32LittleEndian(b[o..], v);
var image = new byte[0x800];
image[0] = (byte)'M'; image[1] = (byte)'Z'; U32(image, 0x3C, 0x80);
image[0x80] = (byte)'P'; image[0x81] = (byte)'E';
var coff = 0x84; U16(image, coff + 2, 1); U16(image, coff + 16, 0xF0);
var optional = coff + 20; U16(image, optional, 0x20B);
var cliEntry = optional + 112 + 14 * 8; U32(image, cliEntry, 0x2100); U32(image, cliEntry + 4, 0x48);
var section = optional + 0xF0; U32(image, section + 8, 0x600); U32(image, section + 12, 0x2000); U32(image, section + 16, 0x600); U32(image, section + 20, 0x200);
var cliOffset = 0x300; U32(image, cliOffset, 0x48); U16(image, cliOffset + 4, 2); U16(image, cliOffset + 6, 5); U32(image, cliOffset + 8, 0x2200); U32(image, cliOffset + 12, 0x100);
var metadataOffset = 0x400; U32(image, metadataOffset, 0x424A5342);
var info = CliPeInspector.Inspect(image);
if (info.MetadataFileOffset != 0x400 || info.MetadataRva != 0x2200) throw new Exception("CLI metadata mapping failed");
var rejected = false; try { CliPeInspector.Inspect(new byte[64]); } catch (InvalidDataException) { rejected = true; }
if (!rejected) throw new Exception("truncated image must fail");
Console.WriteLine("chris-dotnet-pe tests passed");
