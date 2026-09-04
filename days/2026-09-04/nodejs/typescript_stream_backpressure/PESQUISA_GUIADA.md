# Pesquisa guiada
Use a documentação oficial do Node.js sobre `stream.Transform`, `stream.pipeline`, backpressure, `Buffer`, `highWaterMark` e `node:test`.

Para setembro de 2026, Node 24 está em LTS e Node 26 é Current; use LTS em produção salvo necessidade concreta de Current. A implementação deste exercício também roda no Node 22 disponível no container usando type stripping.

Perguntas:
1. Por que uma mensagem TCP pode chegar em múltiplos chunks?
2. O que significa `readableObjectMode: true` aqui?
3. Quem deve controlar a velocidade: o source, o transform ou a cadeia de streams?
4. Qual o risco de usar `Buffer.concat` indefinidamente sem limite?
5. Quando `pipeline()` é preferível a vários `.pipe()` soltos?
