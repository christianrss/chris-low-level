# Resolucao guiada

1. `feed()` apenas acrescenta bytes ao buffer e tenta progredir.
2. Procure `\r\n\r\n`. Se ainda nao chegou, retorne incompleto sem erro.
3. Parseie request line em metodo, target e versao. Uma linha malformada deve falhar explicitamente.
4. Parseie headers por `:` e remova espacos nas bordas.
5. Se houver Content-Length, so finalize quando o corpo inteiro existir.
6. Escreva um teste que divide o Host no meio e outro que divide o body. Esse teste representa o comportamento real de TCP.
7. Adicione caso negativo `BROKEN\r\n\r\n`.
8. Benchmarke req/s do parser isolado; mais tarde compare com custo de socket e alocacoes.

## Etapa de código 1 - buffering

```cpp
bool HttpRequestParser::feed(const std::string& bytes) {
    if (complete_) {
        throw std::logic_error("parser is already complete; call reset first");
    }
    buffer_ += bytes;
    try_parse();
    return complete_;
}
```

## Etapa de código 2 - delimiter de headers

```cpp
const std::size_t header_end = buffer_.find("\r\n\r\n");
if (header_end == std::string::npos) {
    return;
}
```

Só depois parseie request line e headers.

## Etapa de código 3 - corpo incompleto

```cpp
const std::size_t body_start = header_end + 4;
if (buffer_.size() < body_start + content_length) {
    return;
}
request_.body = buffer_.substr(body_start, content_length);
complete_ = true;
```

## Teste fragmentado

```cpp
assert(!parser.feed("POST /x HTTP/1.1\r\nContent-Length: 5\r\n\r\nhe"));
assert(parser.feed("llo"));
assert(parser.request().body == "hello");
```

Esse padrão prepara o componente para sockets reais sem depender de rede durante unit tests. Solução final em `solutions/src/http_parser.cpp`.

