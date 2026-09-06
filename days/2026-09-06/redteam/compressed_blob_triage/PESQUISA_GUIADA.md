# Pesquisa guiada — Compressed blob triage

Leia RFC 1950 (zlib), RFC 1952 (gzip) e documentação Python `gzip.decompress(max_length=...)`. Perguntas:

1. Por que gzip e zlib têm headers diferentes se ambos encapsulam DEFLATE?
2. O que é zip bomb / decompression bomb e como `max_length` mitiga?
3. Compare magic `1F 8B` com assinatura PK zip (`50 4B`).
4. Por que strings ASCII frequentemente aparecem **antes** do blob gzip em malware staging?
5. O que o segundo byte `78 9C` de zlib codifica (nível de compressão)?

## Regra

Use as fontes para **entender e validar**. Não copie implementação pronta para preencher o starter. Registre em poucas linhas o que aprendeu e qual decisão do exercício a fonte ajuda a justificar.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar `RT-COMP-01`, desenhe os primeiros 4 bytes de `gzip.compress(b"test")` e `zlib.compress(b"test")` **sem executar código**. Confira depois. Registre no Relatório de resolução.
