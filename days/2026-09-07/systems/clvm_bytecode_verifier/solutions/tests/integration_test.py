# PEDAGOGY-TEST: CLVM-VFY-BRANCH-01
# PEDAGOGY-TEST: CLVM-VFY-STACK-01
# Caso 1: ok.clvm valid
# Caso 2: bad_checksum rejected
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify_clvm  # noqa: E402


def main() -> int:
    ok = verify_clvm.verify((ROOT / "fixtures" / "ok.clvm").read_bytes())
    if ok:
        print("ok.clvm should be valid", ok, file=sys.stderr)
        return 1
    bad = verify_clvm.verify((ROOT / "fixtures" / "bad_checksum.clvm").read_bytes())
    if "checksum mismatch" not in bad:
        print("expected checksum mismatch", bad, file=sys.stderr)
        return 1
    print("clvm_bytecode_verifier tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
