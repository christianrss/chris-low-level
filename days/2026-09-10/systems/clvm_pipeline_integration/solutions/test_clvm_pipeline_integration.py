# PEDAGOGY-TEST: CAP-CLVM-DIS-01
# PEDAGOGY-TEST: CAP-CLVM-PEEP-02
# PEDAGOGY-TEST: CAP-CLVM-VFY-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from clvm_pipeline_integration import disasm, peephole, verify_stack

def main():
    code = bytes([0x01, 1, 0x01, 2, 0x02, 0x08])
    assert disasm(code) == ["PUSH 1", "PUSH 2", "ADD", "HALT"]
    folded = peephole(bytes([0x01, 0, 0x02, 0x01, 5, 0x08]))
    assert folded == bytes([0x01, 5, 0x08])
    assert verify_stack(code)
    print("OK clvm_pipeline")

if __name__ == "__main__":
    main()
