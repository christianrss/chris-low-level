# Exercícios — HTTP parser

## Fácil

- **HTTP-DELIM-01:** identifique manualmente onde termina o header block em uma requisição GET de exemplo.
- **HTTP-PARSE-01:** implemente detecção de `\r\n\r\n` e parse da request line.

## Médio

- **HTTP-HEADERS-01:** parse headers `Name: Value` com trim de espaços.
- **HTTP-BODY-01:** respeite `Content-Length` aguardando bytes do body.

## Difícil

- **HTTP-FRAG-01:** faça passar o teste que divide `Host:` entre dois `feed()`.
- **HTTP-ERR-01:** trate request line inválida com exceção ou erro conforme teste.

## Desafio

- **HTTP-CHUNK-01:** descreva como adicionaria suporte a `Transfer-Encoding: chunked` sem reescrever tudo.
- **HTTP-BENCH-01:** compare throughput do parser com corpo de 1 KiB vs 1 MiB no benchmark guiado.
