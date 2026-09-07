# PEDAGOGY-TEST: RT-HID-MAGIC-01
# PEDAGOGY-TEST: RT-HID-BOUNDS-02
# PEDAGOGY-TEST: RT-HID-STRINGS-03
# Caso 1: report de 8 bytes válido passa validate_hid_boot_length.
# Caso 2: report de 7 bytes falha MAGIC-01.
# Caso 3: spam de 6 teclas → BOUNDS-02 retorna 6.
# Caso 4: STRINGS-03 lista usage:0x04 para tecla A.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from hid_fuzz import validate_hid_boot_length, count_nonzero_key_slots, extract_hid_usage_hex

def main():
    ok = bytes([0, 0, 0x04, 0, 0, 0, 0, 0])
    assert validate_hid_boot_length(ok)
    assert not validate_hid_boot_length(ok[:7])
    spam = bytes([0, 0, 1, 2, 3, 4, 5, 6])
    assert count_nonzero_key_slots(spam) == 6
    assert extract_hid_usage_hex(ok) == ["usage:0x04"]
    print("OK hid_fuzz")

if __name__ == "__main__":
    main()
