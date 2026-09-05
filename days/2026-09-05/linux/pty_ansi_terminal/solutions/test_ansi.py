# SOLVES [TERM-ANSI-SGR-01]
# SOLVES [TERM-CURSOR-02]
from ansi import Terminal
t=Terminal(); t.feed('A\x1b[31mB\x1b[0m'); assert t.screen_text=='AB' and t.fg==7
t.feed('\x1b[3;5H'); assert (t.row,t.col)==(2,4)
t.feed('\x1b[H'); assert (t.row,t.col)==(0,0)
print('OK ansi')
