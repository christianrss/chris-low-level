# Teoria passo a passo — JavaScript runtime from scratch: branches em bytecode VM

Branches transformam uma VM linear em uma máquina capaz de controle de fluxo. `JZ target` remove/inspeciona condição e altera `ip` quando zero; `JMP target` sempre altera `ip`. O ponto crítico é definir se target é absoluto ou relativo. Hoje usamos **offset absoluto no array de instruções**.
