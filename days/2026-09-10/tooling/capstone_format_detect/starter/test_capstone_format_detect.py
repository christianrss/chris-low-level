# PEDAGOGY-TEST: CAP-TOOL-DET-01
# PEDAGOGY-TEST: CAP-TOOL-DET-02
# PEDAGOGY-TEST: CAP-TOOL-DET-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_format_detect import match_signature, detect_format

def main():
    png = b"\x89PNG\r\n\x1a\n" + b"rest"
    assert match_signature(png) == "PNG"
    d = detect_format(png)
    assert d["format"] == "PNG" and d["confidence"] == 1.0
    print("OK format_detect")

if __name__ == "__main__":
    main()
