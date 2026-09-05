// SOLVES [CLR-IL-OPCODE-01] [CLR-IL-OPERAND-02]
// TESTS [CLR-IL-OPCODE-01] [CLR-IL-OPERAND-02] via asserts em Main
using System.IO;
record Ins(int Offset,string Name,int? Operand);
static List<Ins> Decode(byte[] code){var r=new List<Ins>();for(int i=0;i<code.Length;){int off=i;byte op=code[i++];switch(op){case 0x1F:if(i>=code.Length)throw new InvalidDataException("truncated operand");r.Add(new(off,"ldc.i4.s",unchecked((sbyte)code[i++])));break;case 0x58:r.Add(new(off,"add",null));break;case 0x2A:r.Add(new(off,"ret",null));break;default:throw new InvalidDataException($"unsupported opcode 0x{op:X2}");}}return r;}
var got=Decode(new byte[]{0x1F,0x05,0x1F,0x07,0x58,0x2A});if(got.Count!=4||got[0].Operand!=5||got[2].Name!="add"||got[3].Name!="ret")throw new Exception("assert");try{Decode(new byte[]{0x1F});throw new Exception("truncated accepted");}catch(InvalidDataException){}Console.WriteLine("OK CIL");
