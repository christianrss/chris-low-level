from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_ROOT = ROOT / ".local-build"


def build(name: str) -> Path:
    source = ROOT / "projects" / name
    build_dir = BUILD_ROOT / name
    if not (build_dir / "CMakeCache.txt").exists():
        subprocess.run(
            [
                "cmake",
                "-S",
                str(source),
                "-B",
                str(build_dir),
                "-DCMAKE_BUILD_TYPE=Release",
            ],
            check=True,
        )
        subprocess.run(
            ["cmake", "--build", str(build_dir), "--config", "Release"],
            check=True,
        )
    return build_dir


def executable(build_dir: Path, name: str) -> Path:
    candidates = [
        build_dir / name,
        build_dir / "Release" / f"{name}.exe",
        build_dir / f"{name}.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(name)


vm_build = build("chris-vm")
subprocess.run(
    [
        sys.executable,
        str(ROOT / "projects/chris-vm/benchmarks/benchmark.py"),
        str(executable(vm_build, "clvm")),
    ],
    check=True,
)

subprocess.run(
    [sys.executable, str(ROOT / "projects/chris-autograd/benchmarks/benchmark.py")],
    check=True,
)

dis_build = build("chris-disassembler")
subprocess.run(
    [
        sys.executable,
        str(ROOT / "projects/chris-disassembler/benchmarks/benchmark.py"),
        str(executable(dis_build, "miniobjdump")),
        str(executable(dis_build, "test_target")),
    ],
    check=True,
)

subprocess.run(
    [
        sys.executable,
        str(ROOT / "projects/chris-binary-toolkit/benchmarks/benchmark.py"),
    ],
    check=True,
)

render_build = build("chris-renderer")
subprocess.run(
    [str(executable(render_build, "core_benchmark"))],
    check=True,
)
