# Pesquisa guiada — HTTP/1.x incremental parsing

## Fontes
- RFC 9110 (HTTP Semantics).
- RFC 9112 (HTTP/1.1 message syntax and routing).

## Termos
`HTTP request line CRLF header field content-length`, `incremental HTTP parser fragmented input`, `HTTP message framing security`.

## Perguntas
1. Onde terminam headers em HTTP/1.1?
2. Por que um `feed()` não pode assumir que uma chamada contém uma mensagem completa?
3. Como `Content-Length` determina o fim do body neste subset?
4. Que entradas precisam ser rejeitadas em vez de parcialmente aceitas?
5. Por que parsers de produção têm preocupações de request smuggling que este toy parser não resolve?

Implemente somente o subset declarado no módulo e compare com as RFCs para entender limites e terminologia.
