// PEDAGOGY-TEST [CLR-IL-OPCODE-01]: decode ldc.i4.s, add, ret
// PEDAGOGY-TEST [CLR-IL-OPERAND-02]: operand int8 e truncamento
// PEDAGOGY-SOLUTION: CLR-IL-OPCODE-01
// PEDAGOGY-SOLUTION: CLR-IL-OPERAND-02
using System.IO;

namespace Chris.IlLab;

record Instruction(int Offset, string Name, int? Operand);

static class CilDecoder
{
    public static List<Instruction> Decode(ReadOnlySpan<byte> code)
    {
        var result = new List<Instruction>();
        for (int i = 0; i < code.Length;)
        {
            int offset = i;
            byte opcode = code[i++];

            switch (opcode)
            {
            case 0x1F:
                if (i >= code.Length)
                {
                    throw new InvalidDataException("truncated operand");
                }
                result.Add(new(offset, "ldc.i4.s", unchecked((sbyte)code[i++])));
                break;
            case 0x58:
                result.Add(new(offset, "add", null));
                break;
            case 0x2A:
                result.Add(new(offset, "ret", null));
                break;
            default:
                throw new InvalidDataException($"unsupported opcode 0x{opcode:X2}");
            }
        }
        return result;
    }
}

static class Program
{
    static void Main()
    {
        var instructions = CilDecoder.Decode(
            new byte[] { 0x1F, 0x05, 0x1F, 0x07, 0x58, 0x2A });

        if (instructions.Count != 4
            || instructions[0].Operand != 5
            || instructions[2].Name != "add"
            || instructions[3].Name != "ret")
        {
            throw new Exception("assert");
        }

        try
        {
            CilDecoder.Decode(new byte[] { 0x1F });
            throw new Exception("truncated accepted");
        }
        catch (InvalidDataException)
        {
        }

        Console.WriteLine("OK CIL");
    }
}
