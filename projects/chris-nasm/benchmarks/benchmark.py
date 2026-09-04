from pathlib import Path
import sys, time
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from chris_nasm import assemble

source = "\n".join(["mov rax, 0x12345678", "nop", "mov rdi, 9", "syscall"] * 10000)
for _ in range(3):
    assemble(source)
start = time.perf_counter()
for _ in range(20):
    data = assemble(source)
elapsed = time.perf_counter() - start
lines = 40000 * 20
print(f"lines={lines} seconds={elapsed:.6f} lines_per_second={lines/elapsed:.0f} bytes={len(data)}")
