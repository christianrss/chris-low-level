from pathlib import Path
import subprocess, tempfile, shutil, sys
ROOT=Path(__file__).resolve().parent
expected_fail=[]; unexpected=[]
def cmd_fail(name,cmd,cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    if p.returncode!=0: expected_fail.append(name)
    else: unexpected.append(name+' unexpectedly passed')
def cmake_fail(name,path):
    with tempfile.TemporaryDirectory(prefix='llstarter-') as td:
        c=subprocess.run(['cmake','-S',str(path),'-B',td],capture_output=True,text=True)
        if c.returncode!=0: unexpected.append(name+' configure failed before exercise'); return
        b=subprocess.run(['cmake','--build',td],capture_output=True,text=True)
        if b.returncode!=0: unexpected.append(name+' build failed before test'); return
        cmd_fail(name,['ctest','--test-dir',td,'--output-on-failure'],ROOT)
cmd_fail('linux package',['python3','test_pkg.py'],ROOT/'modules/01_linux_distro_pkg_rootfs/starter')
cmd_fail('linux rootfs',['sh','test_rootfs.sh'],ROOT/'modules/01_linux_distro_pkg_rootfs/starter')
cmake_fail('kernel device model',ROOT/'modules/02_linux_kernel_driver_lifecycle/starter')
cmake_fail('bitmap allocator',ROOT/'modules/03_systems_bitmap_page_allocator/starter')
cmake_fail('tiled matmul',ROOT/'modules/04_ai_tiled_matmul/starter')
cmd_fail('ELF inspector',['python3','test_elf_entry.py'],ROOT/'modules/05_redteam_elf_entry_inspector/starter')
# .NET static only without SDK
if shutil.which('dotnet'): cmd_fail('CIL decoder',['dotnet','run','--project','Chris.IlLab.csproj'],ROOT/'modules/06_dotnet_cil_decoder/starter')
cmd_fail('Node streams',['node','test.js'],ROOT/'modules/07_node_transform_backpressure/starter')
cmd_fail('JS VM',['node','test.js'],ROOT/'modules/08_javascript_bytecode_vm/starter')
cmake_fail('graphics states',ROOT/'modules/09_graphics_resource_states/starter')
cmd_fail('ANSI parser',['python3','test_ansi.py'],ROOT/'modules/10_linux_terminal_ansi/starter')
print('expected starter failures:',len(expected_fail),expected_fail)
if unexpected:
    print('\n'.join('ERROR '+x for x in unexpected));sys.exit(1)
print('STARTER CHECK PASS')
