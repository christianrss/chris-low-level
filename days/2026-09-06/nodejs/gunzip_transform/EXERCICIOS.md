# Exercícios — GunzipTransform

## Fácil

- **ND-GZ-01 (`_transform`):** Encaminhe `chunk` com `this.gunzip.write` e chame `callback` (ou `once('drain', callback)` se `write` retornar false).  
  **Aceite:** round-trip manual de um `gzipSync('hello')` produz `hello`.

- **ND-GZ-01 (`_flush`):** `this.gunzip.end(callback)`.  
  **Aceite:** `await once(transform,'end')` resolve após `transform.end(gz)`.

## Médio

- **ND-GZ-03:** Incremente `bytesIn` em `_transform`; mantenha `bytesOut`/`backpressurePauses` no ctor.  
  **Aceite:** no teste oficial, `bytesIn === gz.length` e `bytesOut > bytesIn`.

## Difícil

- **ND-GZ-02:** Reescreva o loop do demo com `gzipSync`, fatias 64 B e `await once(transform,'drain')`.  
  **Aceite:** `node starter/test.js` imprime `OK gunzip transform` com `falseWrites > 0`.

## Desafio

- **ND-GZ-CH-01:** Instrumente um contador de quantas vezes `_transform` esperou `gunzip` drain (além de `backpressurePauses` do `push`). Documente a diferença entre backpressure **para o gunzip interno** vs **para o Transform downstream**.  
  **Aceite:** tabela com os dois contadores após o demo padrão; texto de 5–10 linhas explicando cada um.
