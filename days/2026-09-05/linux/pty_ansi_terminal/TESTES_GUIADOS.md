# Testes guiados — Linux terminal: ANSI parser como preparação para PTY/TTY

`TERM-ANSI-SGR-01`: `A ESC[31m B ESC[0m` preserva texto `AB` e termina com fg padrão. `TERM-CURSOR-02`: `ESC[3;5H` produz cursor `(2,4)` e defaults são testados. Execute `python starter/test_ansi.py`; solution imprime `OK ansi`.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
