# Testes guiados

### Caso 1: `node starter/test.js` — LineTransform + backpressure integrados.
### Caso 2: **UTF-8 multibyte:** caractere € partido entre chunks → linha `b€`.
### Caso 3: **Backpressure:** `runBackpressureDemo()` deve ter falseWrites > 0 e drains == falseWrites.
### Caso 4: Rode `node backpressure_demo.js` isoladamente para observar stats.
### Caso 5: Valide solutions/ com os mesmos asserts.

## NODE-XFORM-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: NODE-XFORM-01`.

## NODE-BACKPRESSURE-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: NODE-BACKPRESSURE-02`.
