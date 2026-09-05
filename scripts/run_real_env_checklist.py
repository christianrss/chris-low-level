#!/usr/bin/env python3
"""Print real-environment prerequisites and commands for optional module tracks."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKLISTS: dict[str, dict] = {
    "linux/kernel_module_driver_lab": {
        "prereqs": ["linux", "gcc", "make", "kernel headers"],
        "checks": [
            ("uname", ["uname", "-a"]),
            ("gcc", ["gcc", "--version"]),
            ("kernel_headers", ["test", "-d", "/lib/modules/$(uname -r)/build"]),
        ],
        "commands": [
            "cd days/2026-09-05/linux/kernel_module_driver_lab/solutions",
            "# Build out-of-tree module (on Linux with headers):",
            "make -C /lib/modules/$(uname -r)/build M=$PWD modules",
            "sudo insmod chris_char.ko",
            "dmesg | tail -20",
            "sudo rmmod chris_char",
        ],
        "note": "Userspace model (test_device_model) runs everywhere; insmod requires Linux VM.",
    },
    "boot/legacy_bootsector": {
        "prereqs": ["nasm", "qemu-system-x86_64"],
        "checks": [
            ("nasm", ["nasm", "-v"]),
            ("qemu", ["qemu-system-x86_64", "--version"]),
        ],
        "commands": [
            "cd days/2026-09-03/boot/legacy_bootsector/solutions",
            "nasm -f bin src/bootsector.asm -o /tmp/boot.bin",
            "qemu-system-x86_64 -drive format=raw,file=/tmp/boot.bin -display none",
        ],
        "note": "Python tests validate 512-byte layout without QEMU.",
    },
    "dotnet/cil_tiny_decoder": {
        "prereqs": [".NET SDK 8+"],
        "checks": [
            ("dotnet", ["dotnet", "--version"]),
        ],
        "commands": [
            "cd days/2026-09-05/dotnet/cil_tiny_decoder/solutions",
            "dotnet run --project Chris.IlLab.csproj",
        ],
        "note": "Structural tests pass without SDK; execution requires dotnet.",
    },
    "linux/distro_pkg_rootfs": {
        "prereqs": ["bash", "python3", "tar"],
        "checks": [
            ("bash", ["bash", "--version"]),
            ("python", [sys.executable, "--version"]),
        ],
        "commands": [
            "cd days/2026-09-05/linux/distro_pkg_rootfs/solutions",
            "python test_pkg.py",
            "bash test_rootfs.sh",
        ],
        "note": "For chroot: run rootfs script on Linux with fakeroot optional.",
    },
}


def run_check(name: str, cmd: list[str]) -> bool:
    if cmd[0] == "test":
        path = cmd[-1].replace("$(uname -r)", _kernel_release())
        ok = Path(path).exists()
        print(f"  [{'OK' if ok else 'MISS'}] {name}: {path}")
        return ok
    exe = shutil.which(cmd[0])
    if not exe:
        print(f"  [MISS] {name}: {cmd[0]} not in PATH")
        return False
    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=10)
        print(f"  [OK] {name}: {exe}")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        print(f"  [FAIL] {name}: {exe}")
        return False


def _kernel_release() -> str:
    try:
        return subprocess.run(
            ["uname", "-r"], capture_output=True, text=True, check=True, timeout=5
        ).stdout.strip()
    except Exception:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Real-environment checklist for day modules")
    parser.add_argument("--module", required=True, help="e.g. linux/kernel_module_driver_lab")
    parser.add_argument("--day", default="2026-09-05")
    args = parser.parse_args()

    info = CHECKLISTS.get(args.module)
    if not info:
        print(f"No real-env checklist for: {args.module}", file=sys.stderr)
        print("Available:", ", ".join(sorted(CHECKLISTS)), file=sys.stderr)
        return 1

    print(f"# Real-environment checklist: {args.module} (day {args.day})\n")
    print("## Pré-requisitos")
    for p in info["prereqs"]:
        print(f"- {p}")

    print("\n## Verificação")
    results = [run_check(name, cmd) for name, cmd in info["checks"]]

    print("\n## Comandos sugeridos")
    for line in info["commands"]:
        print(line)

    print(f"\n## Nota\n{info['note']}")

    if not all(results):
        print("\nAlguns pré-requisitos faltam — trilha opcional; userspace/CI tests still apply.")
        return 2
    print("\nAmbiente pronto para execução real.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
