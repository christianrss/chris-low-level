# Gabarito — Linux — PTY e Parser ANSI

Respostas esperadas (consulte `solutions/` para código completo).

1. Classe AnsiParser (não Terminal).
2. \x1b[31m define fg=1; \x1b[0m restaura fg=7.
3. \x1b[10;20H → row=9, col=19.
4. screen_text ignora escapes, só literais.
