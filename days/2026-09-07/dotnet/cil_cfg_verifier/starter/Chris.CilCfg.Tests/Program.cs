using Chris.CilCfg; using System.IO;
byte[] ok={0x20,1,0,0,0,0x20,2,0,0,0,0x58,0x2A};
// PEDAGOGY-TEST: D5-CIL-DECODE
// PEDAGOGY-TEST: D5-CIL-WORKLIST
if(Verifier.Verify(ok)!=2) throw new Exception();
// PEDAGOGY-TEST: D5-CIL-MERGE
byte[] bad={0x20,1,0,0,0,0x2D,0x05,0x20,2,0,0,0,0x2A};
try{Verifier.Verify(bad);throw new Exception("expected invalid");}catch(InvalidDataException){}
Console.WriteLine("chris-cil-cfg tests passed");