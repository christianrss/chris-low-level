from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days/2026-09-05"
portable = [
    ("linux/distro_pkg_rootfs", ["python", "test_pkg.py"]),
    ("linux/distro_pkg_rootfs", ["bash", "test_rootfs.sh"]),
    ("redteam/elf_entry_inspector", ["python", "test_elf_entry.py"]),
    ("nodejs/stream_transform_backpressure", ["node", "test.js"]),
    ("javascript/bytecode_branch_vm", ["node", "test.js"]),
    ("linux/pty_ansi_terminal", ["python", "test_ansi.py"]),
]
for relative, command in portable:
    subprocess.run(command, cwd=DAY / relative / "solutions", check=True)

cmake_modules = [
    "linux/kernel_module_driver_lab",
    "systems/bitmap_page_allocator",
    "ai/tiled_matmul_cache",
    "graphics/vulkan_d3d12_resource_states",
]
for relative in cmake_modules:
    project = DAY / relative / "solutions"
    build = project / "build"
    shutil.rmtree(build, ignore_errors=True)
    subprocess.run(
        ["cmake", "-S", str(project), "-B", str(build)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["cmake", "--build", str(build)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["ctest", "--test-dir", str(build), "--output-on-failure"],
        check=True,
    )
print("day03 portable solutions passed")
