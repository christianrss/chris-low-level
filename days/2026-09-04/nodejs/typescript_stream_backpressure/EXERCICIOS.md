# Exercícios — Line framer e backpressure

## Fácil

- Desenhe três chunks (`"hel"`, `"lo\nwor"`, `"ld\n"`) e liste linhas emitidas e conteúdo final de `#pending` após cada chunk.
- Leia `starter/src/line-framer.ts` e explique por que `objectMode: true` no construtor.

## Médio

- **D2-NODE-FRAME-LINES:** implemente busca por `\n`, emissão de linhas completas e retenção apenas do resto em `#pending`.
- Trate chunk vazio como no-op sem emitir linha fantasma.

## Difícil

- Garanta que linha sem `\n` final seja emitida em `_flush` respeitando `maxLineBytes`.
- Explique como `pipeline()` propaga backpressure quando downstream é lento.

## Desafio

- Rode `npm test` e o benchmark em `starter/benchmarks/bench.ts`; registre linhas/s e memória.
- Estenda o framer para aceitar `\r\n` removendo `\r` final da linha emitida.
