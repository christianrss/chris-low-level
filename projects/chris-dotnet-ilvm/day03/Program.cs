// SOLVES [CLR-IL-OPCODE-01]
// SOLVES [CLR-IL-OPERAND-02]
using System.IO;
record Instruction(int Offset,string Name,int? Operand);
static List<Instruction> Decode(ReadOnlySpan<byte> code){ var result=new List<Instruction>(); for(int i=0;i<code.Length;){ int offset=i; byte op=code[i++]; switch(op){ case 0x1F: if(i>=code.Length) throw new InvalidDataException("truncated operand"); var operand=unchecked((sbyte)code[i++]); result.Add(new(offset,"ldc.i4.s",operand)); break; case 0x58: result.Add(new(offset,"add",null)); break; case 0x2A: result.Add(new(offset,"ret",null)); break; default: throw new InvalidDataException($"unsupported opcode 0x{op:X2}"); } } return result; }
var ins=Decode(new byte[]{0x1F,0x05,0x1F,0x07,0x58,0x2A}); if(ins.Count!=4 || ins[0].Operand!=5 || ins[2].Name!="add") throw new Exception("decode"); var neg=Decode(new byte[]{0x1F,0xFF,0x2A}); if(neg[0].Operand!=-1) throw new Exception("signed operand"); try{Decode(new byte[]{0x1F});throw new Exception("truncation accepted");}catch(InvalidDataException){} Console.WriteLine("OK CIL");
