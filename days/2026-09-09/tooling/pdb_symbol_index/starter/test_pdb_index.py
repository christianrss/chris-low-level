# PEDAGOGY-TEST: TL-PDB-PARSE-01
# PEDAGOGY-TEST: TL-PDB-INDEX-02
# PEDAGOGY-TEST: TL-PDB-LOOKUP-03
# Caso 1: parse 1000 main
# Caso 2: index len 2
# Caso 3: lookup main
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pdb_index import parse_symbol_line, build_index, lookup_symbol

def main():
    assert parse_symbol_line("1000 main") == (0x1000, "main")
    idx = build_index(["1000 main", "2000 foo"])
    assert len(idx) == 2
    assert lookup_symbol(idx, 0x1000) == "main"
    print("OK pdb_index")

if __name__ == "__main__":
    main()
