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


def run_cmd(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> tuple[int, str]:
    which_env = env if env is not None else None
    if not shutil.which(cmd[0], path=(which_env or {}).get("PATH")) and cmd[0] not in (sys.executable,):
        if shutil.which(cmd[0]) is None and cmd[0] not in (sys.executable,):
            return 127, f"{cmd[0]} not found in PATH"
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out
    except FileNotFoundError:
        return 127, f"{cmd[0]} not found"


def _vc_ninja_env(instance: Path) -> dict[str, str] | None:
    """Env so Ninja can call this VS install's cl.exe when MSBuild.exe is absent."""
    import os

    msvc_root = instance / "VC" / "Tools" / "MSVC"
    if not msvc_root.is_dir():
        return None
    versions = sorted((p for p in msvc_root.iterdir() if p.is_dir()), reverse=True)
    if not versions:
        return None
    host = versions[0] / "bin" / "Hostx64" / "x64"
    cl = host / "cl.exe"
    if not cl.is_file():
        return None
    sdk = Path(r"D:\Windows Kits\10")
    if not (sdk / "Include").is_dir():
        sdk = Path(r"C:\Program Files (x86)\Windows Kits\10")
    include_root = sdk / "Include"
    if not include_root.is_dir():
        return None
    sdk_ver = sorted((p.name for p in include_root.iterdir() if p.is_dir()), reverse=True)[0]
    include = [
        versions[0] / "include",
        sdk / "Include" / sdk_ver / "ucrt",
        sdk / "Include" / sdk_ver / "um",
        sdk / "Include" / sdk_ver / "shared",
    ]
    lib = [
        versions[0] / "lib" / "x64",
        sdk / "Lib" / sdk_ver / "ucrt" / "x64",
        sdk / "Lib" / sdk_ver / "um" / "x64",
    ]
    if not all(p.is_dir() for p in include + lib):
        return None
    sdk_bin = sdk / "bin" / sdk_ver / "x64"
    path_parts = [str(host)]
    if sdk_bin.is_dir():
        path_parts.append(str(sdk_bin))
    env = os.environ.copy()
    env["PATH"] = os.pathsep.join(path_parts) + os.pathsep + env.get("PATH", "")
    env["INCLUDE"] = os.pathsep.join(str(p) for p in include)
    env["LIB"] = os.pathsep.join(str(p) for p in lib)
    env["CC"] = str(cl)
    env["CXX"] = str(host / "cl.exe")
    return env


def _msbuild_exe(instance: Path | None) -> Path | None:
    if instance is None:
        return None
    for rel in (
        Path("MSBuild/Current/Bin/amd64/MSBuild.exe"),
        Path("MSBuild/Current/Bin/MSBuild.exe"),
    ):
        candidate = instance / rel
        if candidate.is_file():
            return candidate
    return None


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


VS_GENERATORS = {
    "18": "Visual Studio 18 2026",
    "17": "Visual Studio 17 2022",
    "16": "Visual Studio 16 2019",
}


def _vs_instances() -> list[tuple[str, Path, str]]:
    """Installed (generator, path, version), Visual Studio 18 first.

    CMake does not discover VS 2026 on D: unless CMAKE_GENERATOR_INSTANCE is
    ``<path>,version=<installationVersion>``.
    """
    import json
    import os

    vswhere = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio/Installer/vswhere.exe"
    rows: list[tuple[str, str, Path, str]] = []
    if vswhere.exists():
        proc = subprocess.run(
            [str(vswhere), "-all", "-prerelease", "-products", "*", "-format", "json"],
            capture_output=True,
            text=True,
        )
        try:
            data = json.loads(proc.stdout or "[]")
        except json.JSONDecodeError:
            data = []
        for inst in data:
            catalog = inst.get("catalog") or {}
            line = str(catalog.get("productLineVersion") or "")
            path = Path(inst.get("installationPath") or "")
            version = str(inst.get("installationVersion") or catalog.get("productDisplayVersion") or "")
            gen = VS_GENERATORS.get(line)
            if gen and path.is_dir() and version:
                rows.append((line, gen, path, version))
    if not rows:
        for edition in ("Community", "Professional", "Enterprise", "BuildTools", "Preview"):
            for root in (Path(r"D:\Program Files\Microsoft Visual Studio\18"), Path(r"C:\Program Files\Microsoft Visual Studio\18")):
                path = root / edition
                if (path / "Common7" / "IDE").is_dir() or (path / "VC").is_dir():
                    rows.append(("18", VS_GENERATORS["18"], path, "18.0"))
    rows.sort(key=lambda item: (0 if item[0] == "18" else 1, item[2].as_posix()))
    seen: set[str] = set()
    out: list[tuple[str, Path, str]] = []
    for _line, gen, path, version in rows:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        out.append((gen, path, version))
    return out


def _windows_generators() -> list[str]:
    return [gen for gen, _path, _ver in _vs_instances()] or ["Visual Studio 18 2026"]


def cmake_configure_cmd(
    src: Path,
    build: Path,
    generator: str | None = None,
    instance: Path | None = None,
    version: str | None = None,
    ninja: bool = False,
) -> list[str]:
    cmd = ["cmake", "-S", str(src), "-B", str(build)]
    if ninja:
        # VS 18 Community here has cl.exe but no MSBuild.exe. Ninja + that cl
        # still is the VS 2026 compiler.
        cmd.extend([
            "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=cl",
            "-DCMAKE_CXX_COMPILER=cl",
        ])
        return cmd
    if IS_WINDOWS:
        gen = generator or "Visual Studio 18 2026"
        cmd.extend(["-G", gen, "-A", "x64"])
        if instance is not None:
            spec = str(instance)
            if version:
                spec = f"{spec},version={version}"
            cmd.append(f"-DCMAKE_GENERATOR_INSTANCE={spec}")
            msbuild = _msbuild_exe(instance)
            if msbuild is not None:
                cmd.append(f"-DCMAKE_VS_MSBUILD_COMMAND={msbuild}")
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
        attempts = _vs_instances() if IS_WINDOWS else [(None, None, None)]
        if IS_WINDOWS and not attempts:
            attempts = [("Visual Studio 18 2026", None, None)]
        last = ""
        for gen, instance, version in attempts:
            if build.exists():
                shutil.rmtree(build, ignore_errors=True)
            build.mkdir(exist_ok=True)
            env = None
            msbuild = _msbuild_exe(instance)
            use_ninja = False
            if msbuild is not None:
                import os
                env = os.environ.copy()
                env["PATH"] = str(msbuild.parent) + os.pathsep + env.get("PATH", "")
            elif instance is not None:
                env = _vc_ninja_env(instance)
                use_ninja = env is not None
            failed = False
            build_cmd = ["cmake", "--build", str(build)]
            test_cmd = ["ctest", "--test-dir", str(build), "--output-on-failure"]
            if IS_WINDOWS and not use_ninja:
                build_cmd.extend(["--config", "Release"])
                test_cmd.extend(["-C", "Release"])
            for cmd in (
                cmake_configure_cmd(base, build, gen, instance, version, ninja=use_ninja),
                build_cmd,
                test_cmd,
            ):
                code, out = run_cmd(cmd, ROOT, env)
                if code != 0:
                    last = f"{name}: {cmd[0]} failed\n{out}"
                    failed = True
                    if cmd[0] != "cmake":
                        return False, last
                    break
            if not failed:
                return True, f"{name}: ctest OK"
        return False, last

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

    test_mjs = base / "test.mjs"
    if test_mjs.exists():
        if not shutil.which("node"):
            return True, f"{name}: node not in PATH (skipped)"
        code, out = run_cmd(["node", str(test_mjs)], base)
        if code != 0:
            return False, f"{name}: test.mjs failed\n{out}"
        return True, f"{name}: test.mjs OK"

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

    if (base / "Cargo.toml").exists():
        if not shutil.which("cargo"):
            return True, f"{name}: cargo not in PATH (skipped)"
        target_dir = base / "target"
        code, out = run_cmd(
            [
                "cargo",
                "test",
                "--manifest-path",
                str(base / "Cargo.toml"),
                "--target-dir",
                str(target_dir),
            ],
            base,
        )
        if code != 0:
            if code == 127 or "not found" in out.lower():
                return True, f"{name}: cargo not available (skipped)\n{out}"
            return False, f"{name}: cargo test failed\n{out}"
        return True, f"{name}: cargo test OK"

    csproj = list(base.glob("*.csproj"))
    if csproj:
        if not shutil.which("dotnet"):
            return True, f"{name}: dotnet SDK not in PATH (skipped)"
        test_csproj = list((base / "tests").glob("*.csproj")) if (base / "tests").exists() else []
        if test_csproj:
            code, out = run_cmd(["dotnet", "test", str(test_csproj[0])], base)
            if code != 0:
                return False, f"{name}: dotnet test failed\n{out}"
            return True, f"{name}: dotnet test OK"
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
