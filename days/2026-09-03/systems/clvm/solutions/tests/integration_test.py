# PEDAGOGY-TEST [CLVM-PY-FNV-01]: checksum FNV-1a no assemble.py
# PEDAGOGY-TEST [CLVM-ASM-LABELS-01]: labels duas passagens e JMP/JZ
# PEDAGOGY-TEST [CLVM-C-FNV-01]: FNV-1a idêntico ao Python no loader C
# PEDAGOGY-TEST [CLVM-C-HEADER-01]: rejeita flags inválidas e checksum errado
# PEDAGOGY-TEST [CLVM-VM-ARITH-01]: programa arithmetic imprime 38
# PEDAGOGY-TEST [CLVM-VM-JUMP-01]: saltos relativos JMP/JZ no VM
from __future__ import annotations
import subprocess, sys, tempfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: integration_test.py <clvm-exe> <project-root>", file=sys.stderr)
        return 2
    exe = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        image = Path(tmp) / "arithmetic.clvm"
        subprocess.run([sys.executable, str(root / "tools/assemble.py"), str(root / "programs/arithmetic.asm"), str(image)], check=True)
        run = subprocess.run([str(exe), str(image)], text=True, capture_output=True)
        if run.returncode != 0 or run.stdout.strip() != "38":
            print(run.stdout, run.stderr, file=sys.stderr)
            return 1
        data = bytearray(image.read_bytes())
        data[-1] ^= 1
        corrupt = Path(tmp) / "corrupt.clvm"
        corrupt.write_bytes(data)
        bad = subprocess.run([str(exe), str(corrupt)], text=True, capture_output=True)
        if bad.returncode == 0 or "checksum mismatch" not in bad.stderr.lower():
            print("corrupt image was not rejected as expected", file=sys.stderr)
            return 1
    print("chris-vm integration tests passed")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
