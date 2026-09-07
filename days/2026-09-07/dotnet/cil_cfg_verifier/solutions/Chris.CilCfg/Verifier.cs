using System; using System.IO; using System.Collections.Generic; namespace Chris.CilCfg;
public static class Verifier {
 record Ins(int Off,int Size,int Pops,int Pushes,int[] Succ);
 public static int Verify(byte[] code) {
  // PEDAGOGY-SOLUTION: D5-CIL-DECODE
  var ins=new Dictionary<int,Ins>(); int ip=0;
  while(ip<code.Length){int o=ip; byte op=code[ip++]; int pops=0,push=0; int[] succ;
   if(op==0x20){if(ip+4>code.Length)throw new InvalidDataException(); ip+=4;push=1;succ=new[]{ip};}
   else if(op==0x58){pops=2;push=1;succ=new[]{ip};}
   else if(op==0x2B||op==0x2D){if(ip>=code.Length)throw new InvalidDataException(); sbyte d=unchecked((sbyte)code[ip++]);int t=ip+d;pops=op==0x2D?1:0;succ=op==0x2D?new[]{t,ip}:new[]{t};}
   else if(op==0x2A){pops=1;succ=Array.Empty<int>();}
   else throw new InvalidDataException($"opcode {op:X2}");
   ins[o]=new Ins(o,ip-o,pops,push,succ);
  }
  // PEDAGOGY-SOLUTION: D5-CIL-WORKLIST
  var depth=new Dictionary<int,int>{{0,0}};var q=new Queue<int>();q.Enqueue(0);int max=0;
  while(q.Count>0){int o=q.Dequeue();if(!ins.TryGetValue(o,out var x))throw new InvalidDataException("target not instruction");
   int d=depth[o];if(d<x.Pops)throw new InvalidDataException("underflow");int od=d-x.Pops+x.Pushes;max=Math.Max(max,od);
   foreach(var s in x.Succ){if(s==code.Length)throw new InvalidDataException("fallthrough past end");if(!ins.ContainsKey(s))throw new InvalidDataException("target not instruction");
    // PEDAGOGY-SOLUTION: D5-CIL-MERGE
    if(depth.TryGetValue(s,out int old)){if(old!=od)throw new InvalidDataException("incompatible stack depth at merge");}
    else{depth[s]=od;q.Enqueue(s);}
   }}
  return max;
 }}
