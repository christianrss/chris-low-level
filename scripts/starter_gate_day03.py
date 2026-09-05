from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days/2026-09-05"
checks = []


def expect_failure(name: str, command: list[str], cwd: Path) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    checks.append((name, result.returncode != 0))


script_cases = [
    ("linux pkg", "linux/distro_pkg_rootfs", ["python", "test_pkg.py"]),
    ("linux rootfs", "linux/distro_pkg_rootfs", ["bash", "test_rootfs.sh"]),
    ("redteam elf", "redteam/elf_entry_inspector", ["python", "test_elf_entry.py"]),
    (
        "node streams",
        "nodejs/stream_transform_backpressure",
        ["node", "test.js"],
    ),
    ("js vm", "javascript/bytecode_branch_vm", ["node", "test.js"]),
    ("terminal ansi", "linux/pty_ansi_terminal", ["python", "test_ansi.py"]),
]
for name, relative, command in script_cases:
    expect_failure(name, command, DAY / relative / "starter")

cmake_cases = [
    ("kmod model", "linux/kernel_module_driver_lab"),
    ("page allocator", "systems/bitmap_page_allocator"),
    ("matmul", "ai/tiled_matmul_cache"),
    ("gpu states", "graphics/vulkan_d3d12_resource_states"),
]
for name, relative in cmake_cases:
    project = DAY / relative / "starter"
    build = project / "build"
    shutil.rmtree(build, ignore_errors=True)
    configure = subprocess.run(
        ["cmake", "-S", str(project), "-B", str(build)],
        stdout=subprocess.DEVNULL,
    )
    if configure.returncode != 0:
        checks.append((name + " configure", False))
        continue
    compile_result = subprocess.run(
        ["cmake", "--build", str(build)],
        stdout=subprocess.DEVNULL,
    )
    if compile_result.returncode != 0:
        checks.append((name + " build", False))
        continue
    expect_failure(
        name,
        ["ctest", "--test-dir", str(build), "--output-on-failure"],
        project,
    )

failed = [name for name, ok in checks if not ok]
if failed:
    print("starter gate failed: " + ", ".join(failed))
    sys.exit(1)
print(f"starter gate passed: {len(checks)} portable starter checks")
