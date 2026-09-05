# TESTS [TERM-ANSI-SGR-01] [TERM-CURSOR-02]
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));from ansi import AnsiParser
p=AnsiParser();p.feed('A\x1b[31mB\x1b[10;20HC\x1b[0m');assert p.screen_text=='ABC';assert p.row==9 and p.col==19 and p.fg==7;print('OK ANSI')
