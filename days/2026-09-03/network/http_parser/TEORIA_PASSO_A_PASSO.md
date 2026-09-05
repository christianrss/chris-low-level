# Teoria passo a passo — HTTP request parser incremental

## 1. O que estamos construindo

Um parser de requisições HTTP/1.1 que aceita bytes fragmentados (como TCP entrega) e só considera a mensagem completa quando headers e corpo (se houver) foram recebidos.

## 2. Por que parser antes de sockets

TCP é um fluxo de bytes, não mensagens. Separar parsing de rede permite:

- testes unitários determinísticos;
- fuzzing sem abrir portas;
- benchmarks de parsing isolado.

## 3. Máquina de estados interna

```text
buffer acumula bytes
  |
  v
procura CRLF CRLF (\r\n\r\n)
  |
  v
parse request line: METHOD SP TARGET SP VERSION
  |
  v
parse headers: Name: Value (um por linha)
  |
  v
se Content-Length presente:
  aguardar N bytes de body no buffer
senão:
  request completa
```

## 4. Exemplo numérico — GET fragmentado

Chunk 1: `GET /hello HTTP/1.1\r\nHost: ex`
Chunk 2: `ample.test\r\n\r\n`

Após chunk 1: incompleto (`feed` retorna false).
Após chunk 2: `method=GET`, `target=/hello`, `Host=example.test`, body vazio.

POST com corpo:

```text
POST /x HTTP/1.1\r\nContent-Length: 5\r\n\r\nhe
```

+ `llo` → body `hello` (5 bytes exatos).

## 5. Tabela de delimitadores

```text
token          | bytes
---------------|------------------
fim de linha   | 0x0D 0x0A (\r\n)
fim de headers | \r\n\r\n
Content-Length | decimal ASCII, sem sinal
```

## 6. Invariantes

- Não parsear headers até encontrar `\r\n\r\n` completo.
- `Content-Length` ausente ⇒ body vazio neste milestone.
- `Content-Length` presente ⇒ exatamente N bytes após headers; extras ficam para próximo `feed` após `reset`.
- Nomes de header preservados como recebidos (case do lab); valores trimados conforme implementação.

## 7. Complexidade

- Busca de `\r\n\r\n`: O(n) no tamanho do buffer acumulado.
- Parse de headers: O(h) linhas.
- Memória: O(tamanho da requisição) no buffer interno.

## 8. Bugs comuns

- Tratar `\n\n` como fim de headers (HTTP exige `\r\n`).
- Ignorar body parcial e marcar completo cedo.
- Não resetar estado entre requisições na mesma conexão keep-alive futura.
- `stoi` em Content-Length inválido sem erro claro.
- Assumir uma única chamada `feed` por requisição.

## 9. Comparação com produção

| Este parser | nghttp2 / llhttp / hyper |
|-------------|--------------------------|
| HTTP/1.1 subset | HTTP/1.1 completo + HTTP/2 |
| incremental simples | state machine otimizada |
| Content-Length only | chunked, trailers, upgrade |
| sem limite de tamanho | limites anti-DoS |

O padrão “acumular até delimitador” é idêntico em servidores reais.

## 10. Passo a passo guiado

1. Acumule bytes em `buffer_`.
2. Localize `\r\n\r\n` (`HTTP-PARSE-01`).
3. Parse request line e headers.
4. Leia `Content-Length`; aguarde body.
5. `reset()` e teste fragmentação em `starter/tests/test_http.cpp`.

## 11. Como saber se está correto

Testes GET fragmentado e POST com body parcial passam; entrada malformada lança ou retorna erro conforme teste.
## 7. Máquina incremental

```text
READING_HEADERS --(CRLF CRLF)--> READING_BODY --(len bytes)--> MESSAGE_COMPLETE
```

## 8. Exemplo de request

```text
GET /api HTTP/1.1\r\n
Host: localhost\r\n
Content-Length: 4\r\n
\r\n
body
```

## 9. Invariantes

- Sem `\r\n\r\n` não há body confiável.
- `Content-Length` ausente ⇒ body vazio neste milestone.
- Buffer pode conter múltiplos requests parciais.

## 10. Bugs comuns

- Procurar `\n\n` em vez de `\r\n\r\n`.
- Não acumular chunks entre `feed()` calls.
- Interpretar body antes de parsear todos os headers.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
