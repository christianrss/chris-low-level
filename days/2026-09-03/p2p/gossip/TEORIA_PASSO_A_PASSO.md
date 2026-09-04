# Teoria passo a passo - gossip

Gossip replica informacao encaminhando mensagens entre vizinhos. O primeiro problema serio e duplicacao: em um ciclo A-B-C-A, uma mensagem voltaria indefinidamente se cada peer nao guardasse IDs ja vistos. TTL adiciona um limite explicito de propagacao.

A simulacao e deterministica e em memoria. Isso permite testar topologias, falhas e invariantes antes de qualquer socket real.
