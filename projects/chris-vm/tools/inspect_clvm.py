#!/usr/bin/env python3
import argparse, struct
from pathlib import Path

def fnv1a32(data):
    h=0x811C9DC5
    for b in data: h=((h^b)*0x01000193)&0xffffffff
    return h

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file'); a=ap.parse_args()
    d=Path(a.file).read_bytes()
    if len(d)<16: raise SystemExit('too small')
    magic=d[:4]; version,flags=d[4],d[5]; entry,size,checksum=struct.unpack_from('<HII',d,6)
    code=d[16:]
    print(f'magic={magic!r} version={version} flags={flags} entry={entry}')
    print(f'code_size={size} actual={len(code)} checksum=0x{checksum:08x} computed=0x{fnv1a32(code):08x}')
    for off in range(0,len(d),16):
        chunk=d[off:off+16]; hx=' '.join(f'{b:02x}' for b in chunk); asc=''.join(chr(b) if 32<=b<127 else '.' for b in chunk)
        print(f'{off:08x}  {hx:<47}  {asc}')
if __name__=='__main__': main()
