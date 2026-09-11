# PEDAGOGY-TEST: CAP-RT-FMT-01
# PEDAGOGY-TEST: CAP-RT-FMT-02
# PEDAGOGY-TEST: CAP-RT-FMT-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_triage import detect_magic, min_size_for, triage_report

def main():
    assert detect_magic(b"\x7fELF\x02") == "ELF"
    assert detect_magic(b"MZ\x90") == "PE"
    assert detect_magic(b"\x00asm\x01") == "WASM"
    assert min_size_for("PE") == 2
    r = triage_report(b"MZ")
    assert r["ok"] is True
    print("OK triage")

if __name__ == "__main__":
    main()
