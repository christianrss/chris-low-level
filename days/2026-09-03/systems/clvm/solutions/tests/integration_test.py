# PEDAGOGY-TEST [CLVM-PY-FNV-01]: checksum FNV-1a no assemble.py
# PEDAGOGY-TEST [CLVM-ASM-LABELS-01]: labels duas passagens e JMP/JZ
# PEDAGOGY-TEST [CLVM-C-FNV-01]: FNV-1a idêntico ao Python no loader C
# PEDAGOGY-TEST [CLVM-C-HEADER-01]: rejeita flags inválidas e checksum errado
# PEDAGOGY-TEST [CLVM-VM-ARITH-01]: programa arithmetic imprime 38
# PEDAGOGY-TEST [CLVM-VM-JUMP-01]: saltos relativos JMP/JZ no VM
# PEDAGOGY-TEST: CLVM-RS-FNV-01
# PEDAGOGY-TEST: CLVM-RS-HEADER-01
# PEDAGOGY-TEST: CLVM-RS-WALK-01
# Caso 1: compile solutions/.
# Caso 2: assemble.py gera arithmetic.clvm no temp dir.
# Caso 3: execute clvm arithmetic.clvm.
# Caso 4: capture stdout.
# Caso 5: falhe se saída.strip() != "38".
# Caso 6: gere arquivo válido (arithmetic.clvm).
# Caso 7: inverta um bit do último byte sem recalcular checksum.
# Caso 8: execute a VM no arquivo corrompido.
# Caso 9: processo deve falhar e mencionar checksum mismatch.
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_rust_validator_tests(root: Path) -> int:
    cargo = shutil.which("cargo")
    if not cargo:
        print("cargo not in PATH — skipping rust-validator tests")
        return 0
    manifest = root / "rust-validator" / "Cargo.toml"
    if not manifest.exists():
        print("rust-validator missing", file=sys.stderr)
        return 1
    target = root / "rust-validator" / "target"
    proc = subprocess.run(
        [
            cargo,
            "test",
            "--manifest-path",
            str(manifest),
            "--target-dir",
            str(target),
            "--",
            "--nocapture",
        ],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        print(proc.stdout, proc.stderr, file=sys.stderr)
        return 1
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: integration_test.py <clvm-exe> <project-root>", file=sys.stderr)
        return 2
    exe = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        image = Path(tmp) / "arithmetic.clvm"
        subprocess.run(
            [
                sys.executable,
                str(root / "tools/assemble.py"),
                str(root / "programs/arithmetic.asm"),
                str(image),
            ],
            check=True,
        )
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

    if run_rust_validator_tests(root) != 0:
        return 1

    print("clvm integration tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
