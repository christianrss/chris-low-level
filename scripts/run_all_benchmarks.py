from __future__ import annotations
import os, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / '.local-build-bench'
CPP_PROJECTS = {
    'chris-cpu': 'cpu_benchmark',
    'chris-terminal': 'terminal_benchmark',
    'chris-http': 'http_benchmark',
    'chris-driver-lab': 'driver_ring_benchmark',
    'chris-debugger': 'debugger_benchmark',
    'chris-os': 'os_graphics_benchmark',
    'chris-qsim': 'qsim_benchmark',
    'chris-algorithms': 'algorithm_benchmark',
    'chris-tensor': 'tensor_benchmark',
    'chris-arena': 'arena_benchmark',
}
if os.name != 'nt' and os.uname().machine in ('x86_64','amd64'):
    CPP_PROJECTS['chris-assembly-lab'] = 'assembly_benchmark'
for name, exe in CPP_PROJECTS.items():
    build = BUILD / name
    if build.exists(): shutil.rmtree(build)
    subprocess.run(
        [
            'cmake',
            '-S', str(ROOT / 'projects' / name),
            '-B', str(build),
            '-DCMAKE_BUILD_TYPE=Release',
            '-DCHRIS_BUILD_BENCHMARKS=ON',
        ],
        check=True,
    )
    subprocess.run(['cmake','--build',str(build),'--config','Release'],check=True)
    suffix = '.exe' if os.name == 'nt' else ''
    candidates = [build/(exe+suffix), build/'Release'/(exe+suffix)]
    binary = next((p for p in candidates if p.exists()), None)
    if binary: subprocess.run([str(binary)],check=True)
for script in [
    ROOT/'projects/chris-binary-toolkit/benchmarks/elf64_benchmark.py',
    ROOT/'projects/chris-nasm/benchmarks/benchmark.py',
    ROOT/'projects/chris-p2p/benchmarks/benchmark.py',
    ROOT/'projects/chris-chain/benchmarks/benchmark.py',
    ROOT/'projects/chris-autograd/benchmarks/benchmark.py',
]:
    subprocess.run([sys.executable, str(script)], check=True)
