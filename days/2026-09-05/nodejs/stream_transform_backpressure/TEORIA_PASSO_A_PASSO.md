# Teoria passo a passo — Node.js: Transform stream + backpressure observável

Streams existem para processar dados sem carregar tudo em memória. Um `Transform` recebe chunks; boundaries de chunk não coincidem com boundaries de linha ou UTF-8. O decoder `StringDecoder` evita quebrar um caractere multibyte.

Backpressure aparece quando o buffer interno alcança `highWaterMark`: `write()` retorna `false`; o produtor deve aguardar `drain` antes de continuar.
