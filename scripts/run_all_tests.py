from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    "chris-vm",
    "chris-autograd",
    "chris-disassembler",
    "chris-binary-toolkit",
    "chris-renderer",
    "chris-assembly-lab",
    "chris-cpu",
    "chris-nasm",
    "chris-boot",
    "chris-terminal",
    "chris-http",
    "chris-p2p",
    "chris-chain",
    "chris-driver-lab",
]

for name in PROJECTS:
    src = ROOT / "projects" / name
    build = ROOT / ".local-build" / name
    if build.exists():
        shutil.rmtree(build)
    subprocess.run(
        ["cmake", "-S", str(src), "-B", str(build), "-DCMAKE_BUILD_TYPE=Release"],
        check=True,
    )
    subprocess.run(
        ["cmake", "--build", str(build), "--config", "Release"],
        check=True,
    )
    cmd = ["ctest", "--test-dir", str(build), "--output-on-failure"]
    if os.name == "nt":
        cmd += ["-C", "Release"]
    subprocess.run(cmd, check=True)

print("all portable project tests passed")
