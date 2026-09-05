// Test cases (TESTES_GUIADOS.md):
// Caso 1: `python starter/test_ansi.py` — importa `AnsiParser` (não `Terminal`).
// Caso 2: **SGR:** `\x1b[31m` define vermelho; `\x1b[0m` restaura fg=7.
// Caso 3: **Cursor:** `\x1b[10;20H` → row=9, col=19 (0-based).
// Caso 4: **Home:** `\x1b[H` → (0,0).
// Caso 5: **CSI incompleto:** `\x1b[` sem final → ValueError.
// Caso 6: Valide solutions/ com os mesmos testes.
# PEDAGOGY-TEST: TERM-ANSI-SGR-01: SGR reset após cor vermelha
# PEDAGOGY-TEST: TERM-CURSOR-02: posicionamento de cursor 1-based
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ansi import AnsiParser


def test_sgr_and_cursor() -> None:
    parser = AnsiParser()
    parser.feed("A\x1b[31mB\x1b[10;20HC\x1b[0m")
    assert parser.screen_text == "ABC"
    assert parser.row == 9
    assert parser.col == 19
    assert parser.fg == 7


def test_home_cursor() -> None:
    parser = AnsiParser()
    parser.feed("\x1b[3;5H")
    assert (parser.row, parser.col) == (2, 4)
    parser.feed("\x1b[H")
    assert (parser.row, parser.col) == (0, 0)


if __name__ == "__main__":
    test_sgr_and_cursor()
    test_home_cursor()
    print("OK ansi")