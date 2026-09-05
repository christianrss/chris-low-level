# PEDAGOGY-TEST [BOOT-IMAGE-01]: imagem 512B com assinatura 0xAA55 e prefixo BIOS
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_minimal import build_image


def main():
    image = build_image()
    assert len(image) == 512
    assert image[-2:] == b"\x55\xaa"
    assert image[:9] == bytes.fromhex("b4 0e b0 48 cd 10 f4 eb fd")
    assert all(byte == 0 for byte in image[9:510])
    source = (ROOT / "src" / "bootsector.asm").read_text(encoding="utf-8").lower()
    assert "bits 16" in source
    assert "org 0x7c00" in source
    assert "dw 0xaa55" in source
    print("boot image structural tests passed")


if __name__ == "__main__":
    main()
