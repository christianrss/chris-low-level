using Chris.CilCfg; using System.Diagnostics;
var code=new List<byte>();for(int i=0;i<1000;i++){code.Add(0x20);code.AddRange(BitConverter.GetBytes(i));code.Add(0x26);}code.Add(0x20);code.AddRange(BitConverter.GetBytes(0));code.Add(0x2A);
for(int i=0;i<5;i++)Verifier.Verify(code.ToArray());
var xs=new List<double>();for(int i=0;i<30;i++){var s=Stopwatch.StartNew();Verifier.Verify(code.ToArray());s.Stop();xs.Add(s.Elapsed.TotalMilliseconds);}
xs.Sort();Console.WriteLine($"median_ms={xs[15]:F4} min={xs[0]:F4} max={xs[^1]:F4}");
