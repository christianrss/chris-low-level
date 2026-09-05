// TODO MAPPING: [CLR-IL-OPCODE-01] [CLR-IL-OPERAND-02]
using System.IO;
record Ins(int Offset,string Name,int? Operand);
static List<Ins> Decode(byte[] code){var r=new List<Ins>();for(int i=0;i<code.Length;){int off=i;byte op=code[i++];/* TODO dispatch */throw new InvalidDataException($"unsupported opcode 0x{op:X2}");}return r;}
var got=Decode(new byte[]{0x1F,0x05,0x1F,0x07,0x58,0x2A});Console.WriteLine(got.Count);
