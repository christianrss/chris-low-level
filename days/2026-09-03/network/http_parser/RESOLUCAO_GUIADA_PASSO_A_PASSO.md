# Resolução guiada auditada — HTTP request parser incremental

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `HTTP-PARSE-01` | `starter/src/http_parser.cpp` | `HttpRequestParser::try_parse()` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/network/http_parser/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Edite

```text
starter/src/http_parser.cpp
```

Não altere a API do header. O objetivo é fazer `feed()` funcionar mesmo quando TCP entrega request line, headers ou body em fragmentos arbitrários.

## 1. Includes necessários

Depois de `#include "http_parser.hpp"`, adicione:

```cpp
#include <algorithm>
#include <cctype>
#include <sstream>
#include <stdexcept>
```

## 2. Helper `trim`

Antes de `HttpRequestParser::feed`, adicione:

```cpp
static std::string trim(std::string value) {
    while (!value.empty() &&
           std::isspace(static_cast<unsigned char>(value.front()))) {
        value.erase(value.begin());
    }

    while (!value.empty() &&
           std::isspace(static_cast<unsigned char>(value.back()))) {
        value.pop_back();
    }

    return value;
}
```

O cast para `unsigned char` evita comportamento indefinido de `std::isspace` com `char` negativo.

### Por que funciona?
Headers HTTP permitem espaços ao redor do valor; `trim` remove apenas das extremidades sem alterar o meio. `unsigned char` garante que bytes ≥ 0x80 não viram índices negativos em tabelas de locale.

## 3. `feed`

Substitua o corpo por:

```cpp
if (complete_) {
    throw std::logic_error(
        "parser is already complete; call reset first");
}

buffer_ += bytes;
try_parse();
return complete_;
```

`feed()` não supõe que `bytes` contém uma mensagem inteira.

### Por que funciona?
TCP entrega bytes, não mensagens. Acumular em `buffer_` e chamar `try_parse()` a cada chunk permite progresso parcial sem perder fragmentos anteriores. Lançar se `complete_` evita reparse silencioso após request fechado.

## 4. Detecte fim dos headers

Em `try_parse()`:

```cpp
const std::size_t header_end = buffer_.find("\r\n\r\n");
if (header_end == std::string::npos) {
    return;
}
```

Não lance erro por fragmento incompleto.

### Por que funciona?
`\r\n\r\n` é o delimitador canônico entre headers e body em HTTP/1.x. Retornar cedo quando `npos` mantém o parser em estado “aguardando mais dados” em vez de falhar em fragmento legítimo.

## 5. Request line — trecho omitido na resolução antiga

Crie stream apenas da região de headers:

```cpp
std::istringstream stream(buffer_.substr(0, header_end));
std::string line;
```

Leia primeira linha:

```cpp
if (!std::getline(stream, line)) {
    throw std::runtime_error("missing request line");
}

if (!line.empty() && line.back() == '\r') {
    line.pop_back();
}
```

Separe os três tokens:

```cpp
std::istringstream first(line);
if (!(first >> request_.method >> request_.target >> request_.version)) {
    throw std::runtime_error("malformed request line");
}

if (request_.version.rfind("HTTP/", 0) != 0) {
    throw std::runtime_error("unsupported request version syntax");
}
```

### Por que funciona?
`getline` no stream limitado aos headers evita ler o body como linha de texto. Remover `\r` final trata CRLF corretamente. Três tokens com `>>` falham cedo em linhas malformadas como `BROKEN\r\n\r\n`.

## 6. Headers — também precisava do código completo

```cpp
request_.headers.clear();

while (std::getline(stream, line)) {
    if (!line.empty() && line.back() == '\r') {
        line.pop_back();
    }

    const auto colon = line.find(':');
    if (colon == std::string::npos) {
        throw std::runtime_error("malformed header");
    }

    request_.headers[trim(line.substr(0, colon))] =
        trim(line.substr(colon + 1));
}
```

Neste milestone não há folding/múltiplos headers iguais/normalização case-insensitive completa. Não invente suporte que o parser ainda não possui.

### Por que funciona?
Cada linha `Nome: valor` mapeia para um par no `map`. `trim` em nome e valor evita chaves com espaços fantasmas. `colon == npos` rejeita linha sem separador — típico de corrupção ou ataque.

## 7. Content-Length e body fragmentado

```cpp
std::size_t content_length = 0;
const auto it = request_.headers.find("Content-Length");
if (it != request_.headers.end()) {
    content_length = static_cast<std::size_t>(std::stoull(it->second));
}

const std::size_t body_start = header_end + 4;
if (buffer_.size() < body_start + content_length) {
    return;
}

request_.body = buffer_.substr(body_start, content_length);
complete_ = true;
```

### Por que funciona?
`body_start = header_end + 4` pula o delimitador `\r\n\r\n` (4 bytes). Comparar `buffer_.size()` com `body_start + content_length` só marca completo quando todos os bytes do body chegaram — o teste `feed("llo")` após `"...he"` depende disso.

## 8. `request()`

Mantenha a proteção:

```cpp
if (!complete_) {
    throw std::logic_error("request is not complete");
}
return request_;
```

## 9. Teste fragmentado

```cpp
assert(!parser.feed(
    "POST /x HTTP/1.1\r\nContent-Length: 5\r\n\r\nhe"));
assert(parser.feed("llo"));
assert(parser.request().body == "hello");
```

Também teste um header cortado entre dois `feed()`.

## 10. Negativo

```text
BROKEN\r\n\r\n
```

deve lançar `malformed request line`.

## 11. Build/test

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

## 12. Debugging

- body finaliza cedo: observe `body_start`, `content_length`, `buffer_.size()`;
- header some: confira se você parseia só depois de `\r\n\r\n`;
- request fragmentado lança erro: não tente parsear antes de achar o delimitador;
- `std::stoull` lança: inspecione o valor exato de `Content-Length` após `trim`.

A implementação correspondente está em `solutions/src/http_parser.cpp`.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `HTTP-PARSE-01` — `starter/src/http_parser.cpp` → `solutions/src/http_parser.cpp`.
## Relatório de resolução

### O que foi validado

- Todos os TODOs do `starter/` foram implementados na ordem sugerida.
- Testes com marcadores `PEDAGOGY-TEST` passaram na solution.
- O starter continua falhando nos pontos intencionais até o aluno completar cada ID.

### Armadilhas encontradas

- Leia mensagens de `assert` como contrato, não como bug do teste.
- Compare sempre starter vs solution diff por arquivo.
- Documente no benchmark o que *não* foi medido (I/O, rede, GPU, VM).

**Saída esperada:** testes HTTP em `starter/tests/test_http.cpp` passam com feeds fragmentados.

### Próximo passo sugerido

Repita o módulo sem consultar a resolução, cronometrando apenas a fase de implementação. Depois leia `BENCHMARK_GUIADO.md` e registre suas observações na seção **Resultados observados**.
