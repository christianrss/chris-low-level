using System;
using System.Buffers;
namespace Chris.GcProbe;
public static class Probe {
 public static (long bytes,int checksum) MeasureAllocated(Func<int> work){
  // TODO [D6-DN-ALLOC]: warm-up e janela GetAllocatedBytesForCurrentThread.
  return (0,work());
 }
 public static int BuildWithNew(int iterations){
  // TODO [D6-DN-NEW]: aloque byte[256] por iteração.
  return 0;
 }
 public static int BuildWithPool(int iterations){
  // TODO [D6-DN-POOL]: Rent/Span/Return em finally.
  return 0;
 }
}