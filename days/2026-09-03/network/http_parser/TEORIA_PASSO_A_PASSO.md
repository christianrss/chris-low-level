# Teoria passo a passo - HTTP antes dos sockets

Um socket TCP entrega um fluxo de bytes, nao "uma requisicao". Portanto primeiro construiremos um parser que tolera fragmentacao. Cabecalhos terminam em `\r\n\r\n`; depois `Content-Length` informa quantos bytes de corpo ainda faltam neste milestone.

Separar parser de rede permite unit tests, fuzzing e benchmarks sem abrir portas. Depois o mesmo componente sera usado por cliente/servidor localhost.
