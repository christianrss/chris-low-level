import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"solutions"))
from elf_phdr import parse_program_headers
def fixture(n):
 phoff=64;ents=56;raw=phoff+n*ents;d=bytearray(raw+n);d[:4]=b"\x7fELF";d[4]=2;d[5]=1;d[32:40]=phoff.to_bytes(8,"little");d[54:56]=ents.to_bytes(2,"little");d[56:58]=n.to_bytes(2,"little")
 for i in range(n):
  o=phoff+i*ents;d[o:o+4]=(1).to_bytes(4,"little");d[o+8:o+16]=(raw+i).to_bytes(8,"little");d[o+32:o+40]=(1).to_bytes(8,"little");d[o+40:o+48]=(1).to_bytes(8,"little")
 return bytes(d)
d=fixture(128);xs=[]
for _ in range(30):
 t=time.perf_counter_ns();parse_program_headers(d);xs.append((time.perf_counter_ns()-t)/1e6)
print(f"phnum=128 median_ms={statistics.median(xs):.4f} min={min(xs):.4f} max={max(xs):.4f}")
