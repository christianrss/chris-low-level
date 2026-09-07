import tempfile
from pathlib import Path
from proc_snapshot import *
def line(pid,comm,u=10,s=5,start=100):
 f=["S","1"]+["0"]*9+[str(u),str(s)]+["0"]*4+["2","0",str(start)]
 return f"{pid} ({comm}) "+" ".join(f)
# PEDAGOGY-TEST: D5-PROC-PARSE
a=parse_stat(line(42,"worker pool",10,5,100));assert a.comm=="worker pool" and a.utime==10
# PEDAGOGY-TEST: D5-PROC-SCAN
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/"42";p.mkdir();(p/"stat").write_text(line(42,"x"));assert 42 in scan(td)
# PEDAGOGY-TEST: D5-PROC-DELTA
b=parse_stat(line(42,"worker pool",14,7,100));assert cpu_ticks_delta(a,b)==6
print("chris-proc-snapshot tests passed")
