"""Run day benchmarks and write results JSON."""
from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def median(values: list[float]) -> float:
    s = sorted(values)
    n = len(s)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 120) -> tuple[int, str]:
    proc = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def cmake_config_args() -> list[str]:
    args = ["-DCMAKE_BUILD_TYPE=Release"]
    if platform.system() == "Windows":
        args.extend(["-A", "x64"])
    return args


def cmake_build_args() -> list[str]:
    if platform.system() == "Windows":
        return ["--config", "Release"]
    return []


def ctest_config_args() -> list[str]:
    if platform.system() == "Windows":
        return ["-C", "Release"]
    return []


def bench_python_script(script: Path, runs: int = 5) -> dict:
    times: list[float] = []
    last_out = ""
    for _ in range(runs):
        t0 = time.perf_counter()
        code, out = run_cmd([sys.executable, str(script.name)], script.parent)
        elapsed = (time.perf_counter() - t0) * 1000
        if code != 0:
            return {"status": "fail", "script": str(script), "output": out[:500]}
        times.append(elapsed)
        last_out = out.strip().splitlines()[-1] if out.strip() else ""
    parsed: dict = {"status": "ok", "median_ms": round(median(times), 4), "runs": runs}
    if last_out:
        parsed["last_line"] = last_out
        for key in ("MIPS=", "seconds=", "requests_per_second=", "throughput_mib_s="):
            if key in last_out:
                parsed["metric_line"] = last_out
    return parsed


def bench_cmake_module(module: Path, mode: str = "solutions") -> dict | None:
    base = module / mode
    bench_dir = base / "benchmarks"
    if not (base / "CMakeLists.txt").exists():
        return None
    build = base / "build_bench"
    build.mkdir(exist_ok=True)
    cfg = ["cmake", "-S", str(base), "-B", str(build), "-DCHRIS_BUILD_BENCHMARKS=ON"]
    cfg.extend(cmake_config_args())
    code, out = run_cmd(cfg, ROOT)
    if code != 0:
        return {"status": "skip", "reason": f"cmake failed: {out[:200]}"}
    bld = ["cmake", "--build", str(build)] + cmake_build_args()
    code, out = run_cmd(bld, ROOT)
    if code != 0:
        return {"status": "skip", "reason": f"build failed: {out[:200]}"}
    # Find benchmark executables
    exes = list(build.rglob("*bench*"))
    exes = [e for e in exes if e.is_file() and e.suffix in ("", ".exe")]
    if not exes and bench_dir.exists():
        for py in bench_dir.glob("*.py"):
            return bench_python_script(py)
    results: dict = {"status": "ok", "targets": []}
    for exe in exes[:3]:
        times: list[float] = []
        last_line = ""
        for _ in range(3):
            t0 = time.perf_counter()
            code, out = run_cmd([str(exe)], exe.parent)
            elapsed = (time.perf_counter() - t0) * 1000
            if code == 0:
                times.append(elapsed)
                if out.strip():
                    last_line = out.strip().splitlines()[-1]
        if times:
            entry = {"name": exe.name, "median_ms": round(median(times), 4)}
            if last_line:
                entry["last_line"] = last_line
            results["targets"].append(entry)
    return results if results["targets"] else {"status": "skip", "reason": "no bench binary"}


def bench_matmul_day05() -> dict | None:
    base = ROOT / "days" / "2026-09-05" / "ai" / "tiled_matmul_cache" / "solutions"
    if not (base / "bench_matmul.cpp").exists():
        return None
    build = base / "build_bench"
    build.mkdir(exist_ok=True)
    run_cmd(
        ["cmake", "-S", str(base), "-B", str(build), "-DCMAKE_BUILD_TYPE=Release"],
        ROOT,
    )
    run_cmd(["cmake", "--build", str(build)] + cmake_build_args(), ROOT)
    exe = build / "matmul_bench"
    if not exe.exists():
        exe = build / "matmul_bench.exe"
    if not exe.exists():
        return {"status": "skip", "reason": "matmul_bench not built"}
    naive: list[float] = []
    tiled: list[float] = []
    for _ in range(5):
        code, out = run_cmd([str(exe)], exe.parent)
        if code != 0:
            continue
        for line in out.splitlines():
            if "naive_ms=" in line:
                m = re.search(r"naive_ms=([\d.]+)", line)
                if m:
                    naive.append(float(m.group(1)))
            if "tiled16_ms=" in line or "tiled_ms=" in line:
                m = re.search(r"tiled\d*_ms=([\d.]+)", line)
                if m:
                    tiled.append(float(m.group(1)))
    return {
        "matmul_128": {
            "naive_ms": {"median": round(median(naive), 4) if naive else None},
            "tiled16_ms": {"median": round(median(tiled), 4) if tiled else None},
            "runs": len(naive),
        }
    }


def bench_bitmap_day05() -> dict | None:
    base = ROOT / "days" / "2026-09-05" / "systems" / "bitmap_page_allocator" / "solutions"
    if not (base / "CMakeLists.txt").exists():
        return None
    build = base / "build_bench"
    build.mkdir(exist_ok=True)
    cfg = ["cmake", "-S", str(base), "-B", str(build)] + cmake_config_args()
    run_cmd(cfg, ROOT)
    run_cmd(["cmake", "--build", str(build)] + cmake_build_args(), ROOT)
    exe = build / "page_alloc_bench"
    if not exe.exists():
        exe = build / "page_alloc_bench.exe"
    if not exe.exists():
        # Run tests as proxy timing
        test_exe = build / "test_page_allocator"
        if not test_exe.exists():
            test_exe = build / "test_page_allocator.exe"
        if not test_exe.exists():
            return {"status": "skip", "reason": "no bitmap bench binary"}
        times = []
        for _ in range(5):
            t0 = time.perf_counter()
            run_cmd([str(test_exe)], build)
            times.append((time.perf_counter() - t0) * 1000)
        return {"bitmap_tests_ms": {"median": round(median(times), 4), "runs": 5}}
    times = []
    last = ""
    for _ in range(5):
        t0 = time.perf_counter()
        code, out = run_cmd([str(exe)], build)
        times.append((time.perf_counter() - t0) * 1000)
        if out.strip():
            last = out.strip().splitlines()[-1]
    return {
        "bitmap_bench_ms": {"median": round(median(times), 4), "runs": 5, "last_line": last}
    }


def load_existing(day: str) -> dict:
    path = ROOT / "benchmarks" / f"results-{day}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"date": day, "benchmarks": {}, "modules": {}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", required=True)
    parser.add_argument("--update-benchmark-md", action="store_true")
    args = parser.parse_args()

    day_dir = ROOT / "days" / args.day
    results = load_existing(args.day)
    results["generated_at"] = datetime.now(timezone.utc).isoformat()
    results["environment"] = {
        "os": platform.platform(),
        "python": sys.version.split()[0],
    }
    if "modules" not in results:
        results["modules"] = {}

    for module in find_modules(day_dir):
        rel = module.relative_to(day_dir).as_posix()
        r = bench_cmake_module(module)
        if r:
            results["modules"][rel] = r

    if args.day == "2026-09-05":
        mm = bench_matmul_day05()
        if mm:
            results.setdefault("benchmarks", {}).update(mm)
        bm = bench_bitmap_day05()
        if bm:
            results.setdefault("benchmarks", {}).update(bm)

    out_dir = ROOT / "benchmarks"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"results-{args.day}.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"  modules: {len(results.get('modules', {}))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
