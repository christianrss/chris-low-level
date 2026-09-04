#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/solutions"
cmake -S . -B build >/dev/null
cmake --build build >/dev/null
python3 tools/assemble.py programs/arithmetic.asm arithmetic.clvm >/dev/null
python3 tools/assemble.py programs/countdown.asm countdown.clvm >/dev/null
A="$(./build/clvm arithmetic.clvm)"
C="$(./build/clvm countdown.clvm | tr '\n' ' ' | sed 's/ $//')"
[[ "$A" == "38" ]]
[[ "$C" == "3 2 1 0" ]]
python3 tools/inspect_clvm.py arithmetic.clvm | grep -q 'magic=b'
# Corrupt one code byte and ensure parser rejects checksum.
cp arithmetic.clvm corrupt.clvm
python3 - <<'PY'
from pathlib import Path
p=Path('corrupt.clvm'); b=bytearray(p.read_bytes()); b[-1]^=1; p.write_bytes(b)
PY
if ./build/clvm corrupt.clvm >/dev/null 2>&1; then echo 'corruption was not rejected' >&2; exit 1; fi
echo 'smoke tests: PASS'
