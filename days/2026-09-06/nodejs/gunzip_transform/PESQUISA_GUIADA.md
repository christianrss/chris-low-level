# Pesquisa guiada — GunzipTransform

Leia Node.js docs: `stream.Transform`, `stream.backpressure`, `zlib.createGunzip`. Perguntas:

1. Qual diferença entre `pipe()` e encadear manualmente `_transform` + `gunzip`?
2. Quando `writable.write` retorna `false`, o que o produtor deve fazer?
3. Por que `gunzip.pause()` no handler `data` quando `push` retorna false?
4. Compare `pipeline()` com `stream.promises.pipeline` — qual propaga erros melhor?
5. O que `_flush` garante que `_transform` sozinho não garante?

## Regra

Use as fontes para **entender e validar**. Não copie implementação pronta para preencher o starter. Registre em poucas linhas o que aprendeu e qual decisão do exercício a fonte ajuda a justificar.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Desenhe diagrama de eventos: `write → gunzip → data → push → drain → resume`. Só então implemente `ND-GZ-01`.
