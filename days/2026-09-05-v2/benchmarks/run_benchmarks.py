from pathlib import Path
import subprocess, tempfile, time, statistics, json, sys, shutil
ROOT=Path(__file__).resolve().parents[1]
results={}
# package install benchmark: use module's solution functions in-process
sys.path.insert(0,str(ROOT/'modules/01_linux_distro_pkg_rootfs/solutions'))
from chris_pkg import install_package
import json as _json
from tempfile import TemporaryDirectory
samples=[]
for rep in range(11):
    with TemporaryDirectory() as td:
        t=Path(td); pkg=t/'pkg'; (pkg/'payload/usr/share').mkdir(parents=True)
        (pkg/'payload/usr/share/blob.bin').write_bytes(b'x'*4096)
        (pkg/'manifest.json').write_text(_json.dumps({'name':'bench','version':'1','files':['usr/share/blob.bin']}))
        root=t/'root'; s=time.perf_counter(); install_package(pkg,root); e=time.perf_counter()
        if rep>=2: samples.append((e-s)*1000)
results['package_install_4k_ms']={'warmups':2,'repetitions':9,'samples_ms':samples,'median_ms':statistics.median(samples)}
# compile dedicated matmul benchmark with 11 internal repeated invocations via executable runtime
src=ROOT/'modules/04_ai_tiled_matmul/solutions'
build=ROOT/'benchmarks/_build_matmul'
shutil.rmtree(build,ignore_errors=True); build.mkdir(parents=True)
exe=build/'bench_once'
cpp=build/'bench_once.cpp'
cpp.write_text(r"""#include "matmul.hpp"
#include <chrono>
#include <iostream>
#include <vector>
int main(int argc,char**argv){bool tiled=argc>1;size_t n=128;std::vector<float>A(n*n,1),B(n*n,1);auto s=std::chrono::steady_clock::now();auto C=tiled?matmul_tiled(A,B,n,n,n,16):matmul_naive(A,B,n,n,n);auto e=std::chrono::steady_clock::now();std::cout<<std::chrono::duration<double,std::milli>(e-s).count()<<" "<<C[0]<<"\n";}
""")
subprocess.run(['g++','-O2','-std=c++17',str(src/'matmul.cpp'),str(cpp),'-I',str(src),'-o',str(exe)],check=True)
for mode in ['naive','tiled16']:
    vals=[]; checks=[]
    for rep in range(11):
        cmd=[str(exe)]+([] if mode=='naive' else ['tiled'])
        out=subprocess.check_output(cmd,text=True).strip().split(); ms=float(out[0]); checks.append(float(out[1]))
        if rep>=2: vals.append(ms)
    results[f'matmul_128_{mode}_ms']={'warmups':2,'repetitions':9,'samples_ms':vals,'median_ms':statistics.median(vals),'check':checks[-1]}
shutil.rmtree(build,ignore_errors=True)
(ROOT/'benchmarks/results-2026-09-05.json').write_text(json.dumps(results,indent=2))
lines=['# Benchmarks executados - 2026-09-05','', 'Ambiente: container Linux; g++ -O2; 2 warm-ups + 9 repetições. Números não são universais.','']
for k,v in results.items(): lines.append(f"- **{k}**: mediana `{v['median_ms']:.4f} ms`" + (f", check `{v.get('check')}`" if 'check' in v else ''))
(ROOT/'benchmarks/results-2026-09-05.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(results,indent=2))
