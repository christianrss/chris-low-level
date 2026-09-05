# Resolução guiada passo a passo

Abra `starter/line_transform.js`. Em `_transform`, use `this.decoder.write(chunk)`, concatene com `this.pending`, faça `split('\n')`, guarde o último item em pending e faça `push()` nas linhas completas. Em `_flush`, combine `this.pending + this.decoder.end()` e envie o resto se não vazio. Isso fecha `NODE-XFORM-01`.

Agora abra o arquivo real `starter/backpressure_demo.js`. No bloco `if (!ok)`, incremente o contador e adicione:
```js
await once(sink, 'drain');
```
Na solution também contamos `drains` e exigimos `drains === falseWrites`. Isso fecha `NODE-BACKPRESSURE-02`.

Teste:
```bash
node starter/test.js
node starter/backpressure_demo.js
```

Se o teste de UTF-8 falhar, verifique se a divisão acontece antes/depois do decoder. Se backpressure não aparecer, reduza `highWaterMark`.

## Mapa de consistência auditada
- `NODE-XFORM-01` - starter -> resolução -> teste -> solution.
- `NODE-BACKPRESSURE-02` - starter -> resolução -> teste -> solution.
