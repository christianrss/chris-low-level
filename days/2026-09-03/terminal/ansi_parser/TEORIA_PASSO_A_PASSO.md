# Teoria passo a passo - terminal como maquina de estados

Um terminal nao recebe "texto pronto"; recebe bytes. Bytes imprimiveis alteram celulas, enquanto ESC inicia sequencias de controle. `ESC [` introduz CSI. Por isso um terminal e naturalmente um parser incremental: uma leitura pode terminar no meio de uma sequencia e a proxima deve continuar do mesmo estado.

O Day 01 implementa movimentos A/B/C/D, `CSI 2 J` para limpar e reconhece SGR sem aplicar estilo. UTF-8, PTY e modos avancados ficam para milestones posteriores.
