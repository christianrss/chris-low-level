# PEDAGOGY-TEST: CLVM-V2-POOL-01
# PEDAGOGY-TEST: CLVM-V2-PRINTS-01
# Caso 1: hello prints hi
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import clvm_v2  # noqa: E402


def main() -> int:
    img = clvm_v2.assemble_hello()
    if img[4] != 2:
        print("version must be 2", file=sys.stderr)
        return 1
    text = clvm_v2.run_v2(img)
    if text.strip() != "hi":
        print(repr(text), file=sys.stderr)
        return 1
    code, strings = clvm_v2.parse_image(img)
    if strings != ["hi"]:
        print("pool", strings, file=sys.stderr)
        return 1
    print("clvm_v2_strings tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())