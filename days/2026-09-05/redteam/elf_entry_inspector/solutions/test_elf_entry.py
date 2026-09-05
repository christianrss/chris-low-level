# PEDAGOGY-TEST [RT-ELF-HDR-01]: magic, classe e endianness
# PEDAGOGY-TEST [RT-ELF-ENTRY-02]: e_machine e e_entry via offset table
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from elf_entry import ELF64_OFFSETS, parse_elf64, parse_ident


def make_fixture() -> bytes:
    blob = bytearray(64)
    blob[:4] = b"\x7fELF"
    blob[4] = 2
    blob[5] = 1
    blob[6] = 1
    struct.pack_into("<HHIQ", blob, ELF64_OFFSETS["e_type"], 2, 62, 1, 0x401000)
    return bytes(blob)


def test_synthetic_header() -> None:
    header = make_fixture()
    ident = parse_ident(header)
    assert ident["class"] == 64
    result = parse_elf64(header)
    assert result["e_machine"] == 62
    assert result["e_entry"] == 0x401000


def test_fixture_file() -> None:
    fixture = Path(__file__).parent / "fixtures" / "hello_elf64.bin"
    data = fixture.read_bytes()
    result = parse_elf64(data)
    assert result["e_machine"] == 62
    assert result["e_entry"] == 0x401000


def test_rejects_bad_magic() -> None:
    for bad in [b"", b"NOTELF" + bytes(58)]:
        try:
            parse_elf64(bad)
            raise AssertionError("bad data accepted")
        except ValueError:
            pass


if __name__ == "__main__":
    test_synthetic_header()
    test_fixture_file()
    test_rejects_bad_magic()
    print("OK ELF inspector")
