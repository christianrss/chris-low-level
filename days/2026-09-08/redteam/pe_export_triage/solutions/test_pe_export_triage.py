# PEDAGOGY-TEST: RT-PE-EXP-01
# PEDAGOGY-TEST: RT-PE-EXP-02
# PEDAGOGY-TEST: RT-PE-EXP-03
# Caso 1: minimal PE passes validate
# Caso 2: count exports
# Caso 3: flag VirtualAlloc
# Caso 4: invalid returns -1
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pe_export_triage import validate_mz_pe, count_export_names, flag_suspicious_exports

def minimal_pe():
    buf = bytearray(0x100)
    buf[0:2] = b"MZ"
    struct.pack_into("<I", buf, 0x3C, 0x80)
    buf[0x80:0x82] = b"PE"
    return bytes(buf)

def main():
    pe = minimal_pe()
    assert validate_mz_pe(pe)
    assert count_export_names(pe, ["A", "B"]) == 2
    assert flag_suspicious_exports(["VirtualAlloc", "malloc"]) == ["VirtualAlloc"]
    assert count_export_names(b"bad", []) == -1
    print("OK pe_export_triage")

if __name__ == "__main__":
    main()
