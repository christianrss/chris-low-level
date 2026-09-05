from pathlib import Path
import importlib.util
import json
import statistics
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days/2026-09-05"
results = {}

solution = DAY / "ai/tiled_matmul_cache/solutions"
bench_exe = solution / "bench_matmul"
subprocess.run(
    [
        "g++",
        "-O2",
        "-std=c++17",
        str(solution / "matmul.cpp"),
        str(solution / "bench_matmul.cpp"),
        "-o",
        str(bench_exe),
    ],
    check=True,
)
rows = []
for line in subprocess.check_output([str(bench_exe)], text=True).splitlines():
    rows.append(tuple(map(float, line.split())))
results["matmul_128"] = {
    "repetitions": 9,
    "naive_ms": {
        "median": statistics.median(x[0] for x in rows),
        "mean": statistics.mean(x[0] for x in rows),
    },
    "tiled16_ms": {
        "median": statistics.median(x[1] for x in rows),
        "mean": statistics.mean(x[1] for x in rows),
    },
    "compiler": "g++ -O2",
}
bench_exe.unlink(missing_ok=True)

module_path = DAY / "linux/distro_pkg_rootfs/solutions/chris_pkg.py"
spec = importlib.util.spec_from_file_location("chris_pkg", module_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
install_times = []
for _ in range(9):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        package = temp / "pkg"
        (package / "payload/bin").mkdir(parents=True)
        (package / "payload/bin/x").write_bytes(b"x" * 4096)
        manifest = {
            "name": "x",
            "version": "1",
            "files": ["bin/x"],
        }
        (package / "manifest.json").write_text(json.dumps(manifest))
        start = time.perf_counter()
        module.install_package(package, temp / "root")
        install_times.append((time.perf_counter() - start) * 1000.0)
results["chris_pkg_4KiB"] = {
    "repetitions": 9,
    "median_ms": statistics.median(install_times),
    "mean_ms": statistics.mean(install_times),
    "note": "temporary container filesystem; comparison baseline only",
}

(ROOT / "benchmarks/results-2026-09-05.json").write_text(
    json.dumps(results, indent=2) + "\n",
    encoding="utf-8",
)
lines = [
    "# Benchmark results — 2026-09-05",
    "",
    "## Matmul 128x128",
    f"- naive median: {results['matmul_128']['naive_ms']['median']:.3f} ms",
    f"- tiled(16) median: {results['matmul_128']['tiled16_ms']['median']:.3f} ms",
    "- 2 warm-ups; 9 repetitions; g++ -O2.",
    "- Small container-local measurement, not a universal claim.",
    "",
    "## chris-linux-pkg 4 KiB package",
    f"- median install: {results['chris_pkg_4KiB']['median_ms']:.3f} ms",
    "- 9 isolated temporary roots; filesystem/cache effects are confounders.",
]
(ROOT / "benchmarks/results-2026-09-05.md").write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
)
print(json.dumps(results, indent=2))
