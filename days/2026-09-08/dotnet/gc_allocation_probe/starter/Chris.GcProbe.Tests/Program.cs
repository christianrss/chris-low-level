using Chris.GcProbe;
// PEDAGOGY-TEST: D6-DN-ALLOC
var a=Probe.MeasureAllocated(()=>Probe.BuildWithNew(2000));
var p=Probe.MeasureAllocated(()=>Probe.BuildWithPool(2000));
// PEDAGOGY-TEST: D6-DN-NEW
// PEDAGOGY-TEST: D6-DN-POOL
if(a.checksum!=p.checksum) throw new Exception("checksum");
if(a.bytes<=0) throw new Exception("allocation counter");
Console.WriteLine($"chris-gc-probe tests passed new={a.bytes} pool={p.bytes}");
