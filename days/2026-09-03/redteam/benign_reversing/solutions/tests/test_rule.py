# PEDAGOGY-TEST [RE-STRINGS-01]: extração ASCII de runs >=4 bytes
# PEDAGOGY-TEST [RE-YARA-01]: regra YARA identifica binário lab benigno
from pathlib import Path

root = Path(__file__).resolve().parents[1]
text = (root / "rules" / "lab_target.yar").read_text(encoding="utf-8")
required = [
    '"LOWLEVEL-REVERSING-LAB-V1"',
    '"accepted"',
    '"rejected"',
    '$marker and $accepted and $rejected',
]
missing = [token for token in required if token not in text]
if missing:
    raise AssertionError(f"YARA lab rule incomplete; missing: {missing}")
print("YARA rule semantic check: PASS")
