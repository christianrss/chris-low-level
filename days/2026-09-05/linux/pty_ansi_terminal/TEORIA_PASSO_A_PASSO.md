# Teoria passo a passo — Linux terminal: ANSI parser como preparação para PTY/TTY

Um terminal emulator não é o shell. O shell escreve bytes no terminal; sequências ESC/CSI mudam estado de apresentação. PTY será a ponte de processo/TTY em um próximo passo. Hoje construímos o parser determinístico antes de acoplar processos.

Reconhecemos `ESC [ 31 m` (foreground vermelho), `ESC [ 0 m` (reset) e `ESC [ row ; col H` (cursor absoluto, 1-based na sequência e 0-based internamente).
