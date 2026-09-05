# TESTS [RT-ELF-HDR-01] [RT-ELF-ENTRY-02]
import struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));from elf_entry import parse_elf64
b=bytearray(64);b[:4]=b'\x7fELF';b[4]=2;b[5]=1;b[6]=1;struct.pack_into('<HHIQ',b,16,2,62,1,0x401000)
r=parse_elf64(bytes(b));assert r['e_machine']==62 and r['e_entry']==0x401000
for bad in [b'',b'NOTELF'+bytes(58)]:
    try: parse_elf64(bad);raise AssertionError('bad data accepted')
    except ValueError:pass
print('OK ELF inspector')
