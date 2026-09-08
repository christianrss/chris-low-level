using System;
using System.Buffers;
namespace Chris.GcProbe;
public static class Probe {
 public static (long bytes,int checksum) MeasureAllocated(Func<int> work){
  // PEDAGOGY-SOLUTION: D6-DN-ALLOC
  work(); long before=GC.GetAllocatedBytesForCurrentThread(); int checksum=work(); long after=GC.GetAllocatedBytesForCurrentThread(); return(after-before,checksum);
 }
 public static int BuildWithNew(int iterations){
  // PEDAGOGY-SOLUTION: D6-DN-NEW
  int sum=0; for(int i=0;i<iterations;i++){var buffer=new byte[256];buffer[0]=(byte)i;sum+=buffer[0];}return sum;
 }
 public static int BuildWithPool(int iterations){
  // PEDAGOGY-SOLUTION: D6-DN-POOL
  int sum=0; for(int i=0;i<iterations;i++){var buffer=ArrayPool<byte>.Shared.Rent(256);try{var span=buffer.AsSpan(0,256);span[0]=(byte)i;sum+=span[0];}finally{ArrayPool<byte>.Shared.Return(buffer,false);}}return sum;
 }
}