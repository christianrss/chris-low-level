# PEDAGOGY-TEST: OBJDUMP-U16-01
# PEDAGOGY-TEST: OBJDUMP-U32-01
# PEDAGOGY-TEST: OBJDUMP-PARSE-01
from __future__ import annotations
import subprocess, sys, tempfile
from pathlib import Path

def main() -> int:
    if len(sys.argv)!=3:
        print('usage: integration_test.py <miniobjdump> <test_target>', file=sys.stderr); return 2
    tool=Path(sys.argv[1]).resolve(); target=Path(sys.argv[2]).resolve()
    run=subprocess.run([str(tool),str(target)],text=True,capture_output=True)
    if run.returncode!=0:
        print(run.stderr,file=sys.stderr); return 1
    text=run.stdout
    expected='Format: PE' if sys.platform.startswith('win') else 'Format: ELF'
    if expected not in text or '.text' not in text:
        print(text,file=sys.stderr); return 1
    with tempfile.TemporaryDirectory() as tmp:
        bad=Path(tmp)/'bad.bin'; bad.write_bytes(bytes(64))
        failed=subprocess.run([str(tool),str(bad)],text=True,capture_output=True)
        if failed.returncode==0:
            print('invalid file unexpectedly accepted',file=sys.stderr); return 1
    print('chris-disassembler integration tests passed'); return 0
if __name__=='__main__': raise SystemExit(main())
