from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .codegen import CodegenError, compile_to_asm
from .limits import DEFAULT_LIMITS


def _write_clvm(asm_text: str, out: Path) -> None:
    # Import assembler from sibling tools/
    tools_dir = Path(__file__).resolve().parents[1]
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    import assemble  # type: ignore
    import struct

    code = assemble.assemble(asm_text)
    checksum = assemble.fnv1a32(code)
    header = b"CLVM" + bytes([1, 0]) + struct.pack("<HII", 0, len(code), checksum)
    out.write_bytes(header + code)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compile JS subset to CLVM asm or .clvm")
    p.add_argument("input", type=Path, help="source .js")
    p.add_argument("-o", "--output", type=Path, required=True, help="output .asm or .clvm")
    p.add_argument(
        "--emit-clvm",
        action="store_true",
        help="assemble to .clvm directly (reuse assemble.py)",
    )
    p.add_argument(
        "--dump-asm",
        action="store_true",
        help="print generated asm to stdout (in addition to -o)",
    )
    args = p.parse_args(argv)

    source = args.input.read_text(encoding="utf-8")
    try:
        asm = compile_to_asm(source, DEFAULT_LIMITS)
    except (SyntaxError, CodegenError) as exc:
        print(f"js2clvm: {exc}", file=sys.stderr)
        return 1

    if args.dump_asm:
        print(asm, end="")

    if args.emit_clvm:
        _write_clvm(asm, args.output)
        print(f"wrote {args.output}")
    else:
        args.output.write_text(asm, encoding="utf-8")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
