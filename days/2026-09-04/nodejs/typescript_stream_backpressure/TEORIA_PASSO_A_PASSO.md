# Teoria passo a passo

Node não promete que cada `chunk` recebido corresponda a uma mensagem lógica. TCP e streams entregam **sequências de bytes**, então um protocolo precisa fazer framing. O exercício implementa linhas delimitadas por `\n` suportando linhas quebradas entre chunks.

Backpressure aparece quando o consumidor é mais lento que o produtor. Streams do Node propagam esse estado usando seus buffers internos e `highWaterMark`; `pipeline()` coordena completion/error e evita o padrão ruim de “ler tudo em memória e só depois processar”.

O módulo também introduz um limite `maxLineBytes`, porque framing sem limite permite crescimento de memória com uma linha malformada ou atacante.
