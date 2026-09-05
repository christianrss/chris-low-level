# Resolução guiada passo a passo — Node.js: Transform stream + backpressure observável

Abra `starter/line_transform.js`.

Em `_transform`, passe o Buffer ao `StringDecoder.write`, concatene com `this.pending`, separe por `\n`, mantenha o último fragmento em `pending` e faça `push(line)` para linhas completas.

Em `_flush`, use `decoder.end()`, concatene e envie o resto se não vazio.

No exercício `backpressure_demo.js`, escreva em um Writable com `highWaterMark` pequeno. Quando `write()` retornar `false`, incremente `falseWrites`; não continue produzindo sem observar `drain` em aplicações reais. O teste usa esse contador como evidência do mecanismo.

## Mapa de consistência auditada
- `NODE-XFORM-01` — starter → resolução → teste → solution.
- `NODE-BACKPRESSURE-02` — starter → resolução → teste → solution.
