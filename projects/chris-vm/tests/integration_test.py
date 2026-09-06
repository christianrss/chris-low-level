from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def assemble_run(exe: Path, asm: Path, asm_file: Path, out: Path) -> subprocess.CompletedProcess[str]:
    subprocess.run([sys.executable, str(asm), str(asm_file), str(out)], check=True)
    return subprocess.run([str(exe), str(out)], text=True, capture_output=True)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: integration_test.py <clvm-exe> <project-root>", file=sys.stderr)
        return 2
    exe = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    asm = root / "tools" / "assemble.py"
    programs = root / "programs"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        image = tmp_path / "arithmetic.clvm"
        run = assemble_run(exe, asm, programs / "arithmetic.asm", image)
        if run.returncode != 0 or run.stdout.strip() != "38":
            print(run.stdout, run.stderr, file=sys.stderr)
            return 1

        data = bytearray(image.read_bytes())
        data[-1] ^= 1
        corrupt = tmp_path / "corrupt.clvm"
        corrupt.write_bytes(data)
        bad = subprocess.run([str(exe), str(corrupt)], text=True, capture_output=True)
        if bad.returncode == 0 or "checksum mismatch" not in bad.stderr.lower():
            print("corrupt image was not rejected as expected", file=sys.stderr)
            return 1

        add2 = assemble_run(exe, asm, programs / "add2.asm", tmp_path / "add2.clvm")
        if add2.returncode != 0 or add2.stdout.strip() != "8":
            print("add2 failed", add2.stdout, add2.stderr, file=sys.stderr)
            return 1

        mem = assemble_run(exe, asm, programs / "mem_demo.asm", tmp_path / "mem.clvm")
        if mem.returncode != 0 or mem.stdout.strip() != "42":
            print("mem_demo failed", mem.stdout, mem.stderr, file=sys.stderr)
            return 1

        loop = assemble_run(exe, asm, programs / "max_loop.asm", tmp_path / "max_loop.clvm")
        if loop.returncode != 0 or loop.stdout.strip() != "0\n1\n2\n3\n1":
            print("max_loop failed", loop.stdout, loop.stderr, file=sys.stderr)
            return 1

    print("chris-vm integration tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
