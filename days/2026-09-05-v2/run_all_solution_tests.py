from pathlib import Path
import subprocess, shutil, sys, tempfile
ROOT=Path(__file__).resolve().parent
results=[]
def run(name,cmd,cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    status='PASS' if p.returncode==0 else 'FAIL'
    results.append((name,status,p.stdout+p.stderr))
    return p.returncode==0
def cmake_test(name,path,lang=''):
    with tempfile.TemporaryDirectory(prefix='llbuild-') as td:
        if not run(name+' configure',['cmake','-S',str(path),'-B',td],ROOT): return
        if not run(name+' build',['cmake','--build',td],ROOT): return
        run(name,['ctest','--test-dir',td,'--output-on-failure'],ROOT)
run('linux package',['python3','test_pkg.py'],ROOT/'modules/01_linux_distro_pkg_rootfs/solutions')
run('linux rootfs',['sh','test_rootfs.sh'],ROOT/'modules/01_linux_distro_pkg_rootfs/solutions')
cmake_test('kernel device model',ROOT/'modules/02_linux_kernel_driver_lifecycle/solutions')
cmake_test('bitmap allocator',ROOT/'modules/03_systems_bitmap_page_allocator/solutions')
cmake_test('tiled matmul',ROOT/'modules/04_ai_tiled_matmul/solutions')
run('ELF inspector',['python3','test_elf_entry.py'],ROOT/'modules/05_redteam_elf_entry_inspector/solutions')
if shutil.which('dotnet'):
    run('CIL decoder',['dotnet','run','--project','Chris.IlLab.csproj'],ROOT/'modules/06_dotnet_cil_decoder/solutions')
else:
    results.append(('CIL decoder','SKIP','dotnet SDK ausente'))
run('Node streams',['node','test.js'],ROOT/'modules/07_node_transform_backpressure/solutions')
run('Node backpressure demo',['node','backpressure_demo.js'],ROOT/'modules/07_node_transform_backpressure/solutions')
run('JS VM',['node','test.js'],ROOT/'modules/08_javascript_bytecode_vm/solutions')
cmake_test('graphics states',ROOT/'modules/09_graphics_resource_states/solutions')
run('ANSI parser',['python3','test_ansi.py'],ROOT/'modules/10_linux_terminal_ansi/solutions')
print('SUMMARY')
failed=False
for n,s,o in results:
    print(f'{n}: {s}')
    if s=='FAIL': failed=True; print(o)
if failed: sys.exit(1)
