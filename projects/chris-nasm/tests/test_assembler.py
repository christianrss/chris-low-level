from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from chris_nasm import assemble


def main():
    assert assemble("nop\nret\n") == bytes.fromhex("90 c3")
    assert assemble("int3\nsyscall") == bytes.fromhex("cc 0f 05")
    assert assemble("mov rax, 1") == bytes.fromhex("48 b8 01 00 00 00 00 00 00 00")
    assert assemble("mov rdi, 0x1122334455667788") == bytes.fromhex("48 bf 88 77 66 55 44 33 22 11")
    assert assemble("db 0x41, 66, 0x43") == b"ABC"
    try:
        assemble("mov r9, 1")
    except ValueError as exc:
        assert "line 1" in str(exc)
    else:
        raise AssertionError("unsupported register must fail")
    print("chris-nasm tests passed")


if __name__ == "__main__":
    main()
