// Test cases (TESTES_GUIADOS.md):
// Caso 1: Escreva um teste do comportamento mais simples antes de adicionar a feature.
// Caso 2: Rode e observe a falha.
// Caso 3: Implemente apenas o necessario para esse teste.
// Caso 4: Adicione edge case/erro relevante.
// Caso 5: Quando encontrar um bug durante o exercicio, transforme-o em regression test ant
# PEDAGOGY-TEST: BOOT-IMAGE-01
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