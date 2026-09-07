from dataclasses import dataclass
from pathlib import Path
@dataclass(frozen=True)
class Task: pid:int; comm:str; state:str; ppid:int; utime:int; stime:int; num_threads:int; starttime:int
def parse_stat(line):
    # PEDAGOGY-SOLUTION: D5-PROC-PARSE
    lp=line.find("(");rp=line.rfind(")")
    if lp<1 or rp<lp: raise ValueError("bad stat")
    pid=int(line[:lp].strip());comm=line[lp+1:rp];f=line[rp+2:].split()
    if len(f)<20: raise ValueError("short stat")
    return Task(pid,comm,f[0],int(f[1]),int(f[11]),int(f[12]),int(f[17]),int(f[19]))
def scan(root="/proc"):
    # PEDAGOGY-SOLUTION: D5-PROC-SCAN
    out={}
    for p in Path(root).iterdir():
        if not p.name.isdigit(): continue
        try: t=parse_stat((p/"stat").read_text());out[t.pid]=t
        except (FileNotFoundError,PermissionError,ProcessLookupError): pass
    return out
def cpu_ticks_delta(a,b):
    # PEDAGOGY-SOLUTION: D5-PROC-DELTA
    if a.pid!=b.pid or a.starttime!=b.starttime: raise ValueError("process identity changed")
    return (b.utime+b.stime)-(a.utime+a.stime)
