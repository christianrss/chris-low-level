#!/usr/bin/env python3
"""Time N in-process CLVM steps through the xdbg session."""

from __future__ import annotations

import json
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "benchmarks" / "results.json"


def find_exe() -> Path:
    for base in (ROOT / "solutions", ROOT / "starter"):
        for pattern in ("build_ci/**/clvm-xdbg.exe", "build_ci/**/clvm-xdbg", "build/**/clvm-xdbg.exe"):
            matches = list(base.glob(pattern))
            if matches:
                return matches[0]
    raise FileNotFoundError("build clvm-xdbg first (solutions/ preferred)")


def assemble_spin(dest: Path) -> None:
    script = ROOT / "solutions" / "tools" / "assemble.py"
    if not script.exists():
        script = ROOT / "starter" / "tools" / "assemble.py"
    src = ROOT / "solutions" / "programs" / "spin.asm"
    if not src.exists():
        src = ROOT / "starter" / "programs" / "spin.asm"
    subprocess.check_call([sys.executable, str(script), str(src), str(dest)])


def sample_ns(exe: Path, image: Path, steps: int) -> int:
    proc = subprocess.run(
        [str(exe), str(image), "--bench", str(steps)],
        capture_output=True,
        text=True,
        check=True,
    )
    for token in proc.stdout.split():
        if token.startswith("ns="):
            return int(token.split("=", 1)[1])
    raise RuntimeError(proc.stdout + proc.stderr)


def main() -> None:
    exe = find_exe()
    steps = 20000
    samples: list[int] = []
    with tempfile.TemporaryDirectory() as raw:
        image = Path(raw) / "spin.clvm"
        assemble_spin(image)
        for _ in range(7):
            samples.append(sample_ns(exe, image, steps))
    payload = {
        "steps": steps,
        "samples": samples,
        "median": statistics.median(samples),
        "p95": sorted(samples)[int(0.95 * (len(samples) - 1))],
        "unit": "ns",
        "hypothesis": "20k fetch/decode/execute steps stay well under one second on this host.",
    }
    RESULTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
