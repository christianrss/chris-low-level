# PEDAGOGY-TEST: CLVM-EXT-01
# PEDAGOGY-TEST: CLVM-EXT-02
# PEDAGOGY-TEST: CLVM-EXT-03
# PEDAGOGY-TEST: CLVM-EXT-04
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def assemble_run(exe: Path, asm_tool: Path, asm: Path, out: Path) -> subprocess.CompletedProcess[str]:
    subprocess.run([sys.executable, str(asm_tool), str(asm), str(out)], check=True)
    return subprocess.run([str(exe), str(out)], text=True, capture_output=True)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: integration_test.py <clvm-exe> <project-root>", file=sys.stderr)
        return 2
    exe = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    asm_tool = root / "tools" / "assemble.py"
    programs = root / "programs"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        add2 = assemble_run(exe, asm_tool, programs / "add2.asm", tmp_path / "add2.clvm")
        if add2.returncode != 0 or add2.stdout.strip() != "8":
            print("add2 failed", add2.stdout, add2.stderr, file=sys.stderr)
            return 1

        bad_ret = assemble_run(exe, asm_tool, programs / "bad_ret.asm", tmp_path / "bad_ret.clvm")
        if bad_ret.returncode == 0 or "return stack underflow" not in bad_ret.stderr.lower():
            print("expected return stack underflow", bad_ret.stdout, bad_ret.stderr, file=sys.stderr)
            return 1

        mem = assemble_run(exe, asm_tool, programs / "mem_demo.asm", tmp_path / "mem.clvm")
        if mem.returncode != 0 or mem.stdout.strip() != "42":
            print("mem_demo failed", mem.stdout, mem.stderr, file=sys.stderr)
            return 1

        bad_mem = assemble_run(exe, asm_tool, programs / "bad_mem.asm", tmp_path / "bad_mem.clvm")
        if bad_mem.returncode == 0 or "memory out of bounds" not in bad_mem.stderr.lower():
            print("expected memory out of bounds", bad_mem.stdout, bad_mem.stderr, file=sys.stderr)
            return 1

        loop = assemble_run(exe, asm_tool, programs / "max_loop.asm", tmp_path / "max_loop.clvm")
        expected = "0\n1\n2\n3\n1"
        if loop.returncode != 0 or loop.stdout.strip() != expected:
            print("max_loop failed", loop.stdout, loop.stderr, file=sys.stderr)
            return 1

        arith = assemble_run(exe, asm_tool, programs / "arithmetic.asm", tmp_path / "arith.clvm")
        if arith.returncode != 0 or arith.stdout.strip() != "38":
            print("arithmetic regression failed", arith.stdout, arith.stderr, file=sys.stderr)
            return 1

    print("clvm_extended integration tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
