# PEDAGOGY-TEST: RT-YARA-PARSE-01
# PEDAGOGY-TEST: RT-YARA-MATCH-02
# PEDAGOGY-TEST: RT-YARA-TRIAGE-03
# Caso 1: parse AA ??
# Caso 2: match offset 1
# Caso 3: scan_all retorna [1]
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yara_scan import parse_hex_pattern, match_at, scan_all

def main():
    pat = parse_hex_pattern("{ AA ?? }")
    assert pat == [0xAA, None]
    data = bytes([0, 0xAA, 0x55])
    assert match_at(data, pat, 1)
    assert scan_all(data, pat) == [1]
    print("OK yara_scan")

if __name__ == "__main__":
    main()
