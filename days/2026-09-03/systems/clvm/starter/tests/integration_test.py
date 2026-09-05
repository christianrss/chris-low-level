// Test cases (TESTES_GUIADOS.md):
// Caso 1: Compile `solutions/`.
// Caso 2: Use `tools/assemble.py` para gerar `arithmetic.clvm` dentro do diretório de buil
// Caso 3: Execute `clvm arithmetic.clvm`.
// Caso 4: Capture `stdout`.
// Caso 5: Falhe o teste se a saída, removendo espaços finais, não for `38`.
// Caso 6: Gere um arquivo válido.
// Caso 7: Inverta um bit do último byte sem recalcular o checksum.
// Caso 8: Execute a VM.
// Caso 9: O processo deve terminar com erro e mencionar `checksum mismatch`.
# PEDAGOGY-TEST: CLVM-PY-FNV-01
# PEDAGOGY-TEST: CLVM-ASM-LABELS-01
# PEDAGOGY-TEST: CLVM-C-FNV-01
# PEDAGOGY-TEST: CLVM-C-HEADER-01
# PEDAGOGY-TEST: CLVM-VM-ARITH-01
# PEDAGOGY-TEST: CLVM-VM-JUMP-01
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