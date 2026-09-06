// PEDAGOGY-TEST: CLR-IL-OPCODE-01
// TODO [CLR-IL-OPCODE-01]: implement CIL decode dispatch
using System.IO;
record Ins(int Offset, string Name, int? Operand);
static List<Ins> Decode(byte[] code)
{
    var r = new List<Ins>();
    for (int i = 0; i < code.Length;)
    {
        int off = i;
        byte op = code[i++];
        // TODO [CLR-IL-OPCODE-01]: map opcode to instruction
        throw new InvalidDataException($"unsupported opcode 0x{op:X2}");
    }
    return r;
}
var got = Decode(new byte[] { 0x1F, 0x05, 0x1F, 0x07, 0x58, 0x2A });
Console.WriteLine(got.Count);
