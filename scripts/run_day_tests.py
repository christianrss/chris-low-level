"""Run starter or solution tests for a given day."""
from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IS_WINDOWS = platform.system() == "Windows"


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str]:
    if not shutil.which(cmd[0]) and cmd[0] not in (sys.executable,):
        return 127, f"{cmd[0]} not found in PATH"
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out
    except FileNotFoundError:
        return 127, f"{cmd[0]} not found"


def cmake_build_cmd(build_dir: Path) -> list[str]:
    cmd = ["cmake", "--build", str(build_dir)]
    if IS_WINDOWS:
        cmd.extend(["--config", "Release"])
    return cmd


def ctest_cmd(build_dir: Path) -> list[str]:
    cmd = ["ctest", "--test-dir", str(build_dir), "--output-on-failure"]
    if IS_WINDOWS:
        cmd.extend(["-C", "Release"])
    return cmd


def cmake_configure_cmd(src: Path, build: Path) -> list[str]:
    cmd = ["cmake", "-S", str(src), "-B", str(build)]
    if IS_WINDOWS:
        cmd.extend(["-A", "x64"])
    else:
        cmd.append("-DCMAKE_BUILD_TYPE=Release")
    return cmd


def run_module(module: Path, mode: str) -> tuple[bool, str]:
    base = module / mode
    name = module.relative_to(ROOT).as_posix()

    if (base / "CMakeLists.txt").exists():
        build = base / "build_ci"
        if build.exists() and (build / "CMakeCache.txt").exists():
            cache = (build / "CMakeCache.txt").read_text(encoding="utf-8", errors="ignore")
            if IS_WINDOWS and "Visual Studio" not in cache and "-A x64" in " ".join(cmake_configure_cmd(base, build)):
                import shutil as sh
                sh.rmtree(build, ignore_errors=True)
        build.mkdir(exist_ok=True)
        for cmd in (
            cmake_configure_cmd(base, build),
            cmake_build_cmd(build),
            ctest_cmd(build),
        ):
            code, out = run_cmd(cmd, ROOT)
            if code != 0:
                return False, f"{name}: {cmd[0]} failed\n{out}"
        return True, f"{name}: ctest OK"

    for test_py in list(base.glob("test_*.py")) + list(base.glob("tests/test_*.py")):
        code, out = run_cmd([sys.executable, str(test_py)], base)
        if code != 0:
            return False, f"{name}: {test_py.name} failed\n{out}"
        return True, f"{name}: {test_py.name} OK"

    test_js = base / "test.js"
    if test_js.exists():
        if not shutil.which("node"):
            return True, f"{name}: node not in PATH (skipped)"
        code, out = run_cmd(["node", str(test_js)], base)
        if code != 0:
            return False, f"{name}: test.js failed\n{out}"
        return True, f"{name}: test.js OK"

    if (base / "package.json").exists():
        if not shutil.which("npm"):
            return True, f"{name}: npm not in PATH (skipped)"
        if not (base / "node_modules").exists():
            code, out = run_cmd(["npm", "install", "--silent"], base)
            if code != 0:
                if code == 127 or "not found" in out.lower():
                    return True, f"{name}: npm not available (skipped)\n{out}"
                return False, f"{name}: npm install failed\n{out}"
        code, out = run_cmd(["npm", "test"], base)
        if code != 0:
            if code == 127 or "not found" in out.lower():
                return True, f"{name}: npm not available (skipped)\n{out}"
            return False, f"{name}: npm test failed\n{out}"
        return True, f"{name}: npm test OK"

    csproj = list(base.glob("*.csproj"))
    if csproj:
        if not shutil.which("dotnet"):
            return True, f"{name}: dotnet SDK not in PATH (skipped)"
        code, out = run_cmd(["dotnet", "run", "--project", str(csproj[0])], base)
        if code != 0:
            return False, f"{name}: dotnet run failed (SDK may be absent)\n{out}"
        return True, f"{name}: dotnet run OK"

    sh_tests = list(base.glob("test_*.sh"))
    for sh in sh_tests:
        bash = shutil.which("bash")
        if not bash:
            return True, f"{name}: bash not in PATH (skipped {sh.name})"
        code, out = run_cmd([bash, str(sh)], base)
        if code != 0:
            return False, f"{name}: {sh.name} failed\n{out}"
        return True, f"{name}: {sh.name} OK"

    return True, f"{name}: no automated runner (skipped)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", required=True)
    parser.add_argument("--mode", choices=["starter", "solutions"], default="solutions")
    parser.add_argument("--expect-fail", action="store_true", help="For starter mode: failure is OK")
    args = parser.parse_args()

    day_dir = ROOT / "days" / args.day
    if not day_dir.exists():
        print(f"Day not found: {day_dir}", file=sys.stderr)
        return 1

    failures: list[str] = []
    passes: list[str] = []
    for module in find_modules(day_dir):
        ok, msg = run_module(module, args.mode)
        if ok:
            passes.append(msg)
            print(f"PASS: {msg}")
        elif args.expect_fail and args.mode == "starter":
            passes.append(f"EXPECTED FAIL: {msg}")
            print(f"EXPECTED FAIL: {msg}")
        else:
            failures.append(msg)
            print(f"FAIL: {msg}")

    print(f"\n{len(passes)} passed, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
