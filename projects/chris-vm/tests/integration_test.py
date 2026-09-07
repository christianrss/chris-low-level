from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def assemble_run(exe: Path, asm: Path, asm_file: Path, out: Path) -> subprocess.CompletedProcess[str]:
    subprocess.run([sys.executable, str(asm), str(asm_file), str(out)], check=True)
    return subprocess.run([str(exe), str(out)], text=True, capture_output=True)


def js_run(exe: Path, root: Path, js_file: Path, out_clvm: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "tools")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "js2clvm",
            str(js_file),
            "--emit-clvm",
            "-o",
            str(out_clvm),
        ],
        check=True,
        env=env,
        cwd=str(root),
    )
    return subprocess.run([str(exe), str(out_clvm)], text=True, capture_output=True)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: integration_test.py <clvm-exe> <project-root>", file=sys.stderr)
        return 2
    exe = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    asm = root / "tools" / "assemble.py"
    programs = root / "programs"
    examples = root / "examples" / "js"
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

        # JS goldens
        js_add = js_run(exe, root, examples / "add.js", tmp_path / "js_add.clvm")
        if js_add.returncode != 0 or js_add.stdout.strip() != "38":
            print("js add.js failed", js_add.stdout, js_add.stderr, file=sys.stderr)
            return 1

        js_loop = js_run(exe, root, examples / "loop.js", tmp_path / "js_loop.clvm")
        if js_loop.returncode != 0 or js_loop.stdout.strip() != "0\n1\n2\n3":
            print("js loop.js failed", js_loop.stdout, js_loop.stderr, file=sys.stderr)
            return 1

        js_fn = js_run(exe, root, examples / "fn_add.js", tmp_path / "js_fn.clvm")
        if js_fn.returncode != 0 or js_fn.stdout.strip() != "8":
            print("js fn_add.js failed", js_fn.stdout, js_fn.stderr, file=sys.stderr)
            return 1

        js_mod = js_run(exe, root, examples / "mod.js", tmp_path / "js_mod.clvm")
        if js_mod.returncode != 0 or js_mod.stdout.strip() != "2":
            print("js mod.js failed", js_mod.stdout, js_mod.stderr, file=sys.stderr)
            return 1

        # verify tool on a known-good image
        ver = subprocess.run(
            [sys.executable, str(root / "tools" / "verify_clvm.py"), str(tmp_path / "js_add.clvm")],
            text=True,
            capture_output=True,
        )
        if ver.returncode != 0:
            print("verify_clvm failed", ver.stdout, ver.stderr, file=sys.stderr)
            return 1

    print("chris-vm integration tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
