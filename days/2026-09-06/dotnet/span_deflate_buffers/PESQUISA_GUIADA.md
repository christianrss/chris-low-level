# Pesquisa guiada — Span deflate buffers

Leia RFC 1951 seção 3.2.3 (non-compressed blocks) e documentação Microsoft `ReadOnlySpan<T>`. Perguntas:

1. Por que DEFLATE exige `LEN` e `NLEN` complementares em blocos stored?
2. Qual diferença entre BTYPE=00 (stored) e BTYPE=01 (fixed Huffman)?
3. Por que `Span.Slice` não aloca heap?
4. Como `System.IO.Compression.DeflateStream` se relaciona com este parser manual?
5. Em gzip, onde começa o stream DEFLATE após o header `1F 8B 08`?

## Regra

Use as fontes para **entender e validar**. Não copie implementação pronta para preencher o starter. Registre em poucas linhas o que aprendeu e qual decisão do exercício a fonte ajuda a justificar.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Monte manualmente o hex de um bloco stored para payload `"AB"` (2 bytes) incluindo LEN/NLEN. Só então implemente `DN-SPAN-01`.
