# PEDAGOGY-TEST [TERM-ANSI-SGR-01]: SGR reset após cor vermelha
# PEDAGOGY-TEST [TERM-CURSOR-02]: posicionamento de cursor 1-based
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
