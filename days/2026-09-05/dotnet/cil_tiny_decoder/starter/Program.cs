// PEDAGOGY-TEST [CLR-IL-OPCODE-01]: decode ldc.i4.s, add, ret
// PEDAGOGY-TEST [CLR-IL-OPERAND-02]: operand int8 e truncamento
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `dotnet run` em starter/ (falha até decodificar opcodes).
// Caso 2: Bytecode `1F 05 1F 07 58 2A` → 4 instruções: ldc.i4.s 5, ldc.i4.s 7, add, ret.
// Caso 3: **Truncado:** `Decode([0x1F])` → InvalidDataException.
// Caso 4: Consulte TEORIA para mapeamento ECMA-335 Partition III.
// Caso 5: Valide solutions/ com asserts completos.
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

            // TODO [CLR-IL-OPCODE-01]: reconhecer ldc.i4.s, add e ret
            // TODO [CLR-IL-OPERAND-02]: consumir int8 assinado após 0x1F
            switch (opcode)
            {
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
            throw new Exception("decode count");
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
