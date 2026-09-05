import struct
from elf_entry import parse_elf64


def fixture() -> bytes:
    data = bytearray(64)
    data[:4] = b"\x7fELF"
    data[4] = 2
    data[5] = 1
    data[6] = 1
    struct.pack_into("<HHIQ", data, 16, 2, 62, 1, 0x401000)
    return bytes(data)


result = parse_elf64(fixture())
assert result["machine"] == 62
assert result["entry"] == 0x401000

for index, bad_value in ((0, 0), (4, 1), (5, 2)):
    data = bytearray(fixture())
    data[index] = bad_value
    try:
        parse_elf64(bytes(data))
        raise AssertionError(f"invalid ident accepted at index {index}")
    except ValueError:
        pass

print("OK elf entry")
