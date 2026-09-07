# PEDAGOGY-TEST: CLVM-JS-LET-01
# PEDAGOGY-TEST: CLVM-JS-WHILE-01
# PEDAGOGY-TEST: CLVM-JS-CALL-01
# Caso 1: add.js produces STORE/MUL and valid .clvm
# Caso 2: loop.js produces JZ/JMP cycle
# Caso 3: fn_add.js produces CALL
from __future__ import annotations

import struct
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from js2clvm.codegen import compile_to_asm  # noqa: E402
import assemble  # noqa: E402
import verify_clvm  # noqa: E402


def compile_file(js: Path) -> str:
    return compile_to_asm(js.read_text(encoding="utf-8"))


def to_clvm(asm: str, out: Path) -> None:
    code = assemble.assemble(asm)
    checksum = assemble.fnv1a32(code)
    header = b"CLVM" + bytes([1, 0]) + struct.pack("<HII", 0, len(code), checksum)
    out.write_bytes(header + code)


def main() -> int:
    examples = ROOT / "examples" / "js"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        add_asm = compile_file(examples / "add.js")
        if "STORE" not in add_asm or "MUL" not in add_asm:
            print("add.js asm missing STORE/MUL", file=sys.stderr)
            return 1
        add_clvm = tmp_path / "add.clvm"
        to_clvm(add_asm, add_clvm)
        errs = verify_clvm.verify(add_clvm.read_bytes())
        if errs:
            print("add verify", errs, file=sys.stderr)
            return 1

        loop_asm = compile_file(examples / "loop.js")
        if "JZ" not in loop_asm or "JMP" not in loop_asm:
            print("loop.js asm missing JZ/JMP", file=sys.stderr)
            return 1
        to_clvm(loop_asm, tmp_path / "loop.clvm")
        if verify_clvm.verify((tmp_path / "loop.clvm").read_bytes()):
            print("loop verify failed", file=sys.stderr)
            return 1

        fn_asm = compile_file(examples / "fn_add.js")
        if "CALL add" not in fn_asm:
            print("fn_add.js missing CALL", file=sys.stderr)
            return 1
        to_clvm(fn_asm, tmp_path / "fn.clvm")
        if verify_clvm.verify((tmp_path / "fn.clvm").read_bytes()):
            print("fn verify failed", file=sys.stderr)
            return 1

    print("clvm_js_codegen integration tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
