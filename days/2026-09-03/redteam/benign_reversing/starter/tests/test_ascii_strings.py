# PEDAGOGY-TEST: RE-STRINGS-01
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from ascii_strings import extract_ascii_strings

def main() -> int:
    assert extract_ascii_strings(b'\x00HELLO_LOW_LEVEL\x00',5)==[(1,'HELLO_LOW_LEVEL')]
    assert extract_ascii_strings(b'ABCD\x00ABCDE\x00',5)==[(5,'ABCDE')]
    assert extract_ascii_strings(b'',5)==[]
    assert extract_ascii_strings(b'ABC\x01DEF',3)==[(0,'ABC'),(4,'DEF')]
    print('chris-binary-toolkit tests passed'); return 0
if __name__=='__main__': raise SystemExit(main())
