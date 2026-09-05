using System.IO;
record Instruction(int Offset,string Name,int? Operand);
static List<Instruction> Decode(ReadOnlySpan<byte> code){ var result=new List<Instruction>(); for(int i=0;i<code.Length;){ int offset=i; byte op=code[i++]; /* TODO [CLR-IL-OPCODE-01] + [CLR-IL-OPERAND-02] */ throw new InvalidDataException($"unsupported opcode 0x{op:X2}"); } return result; }
var ins=Decode(new byte[]{0x1F,0x05,0x1F,0x07,0x58,0x2A}); if(ins.Count!=4) throw new Exception("decode count"); Console.WriteLine("OK CIL");
