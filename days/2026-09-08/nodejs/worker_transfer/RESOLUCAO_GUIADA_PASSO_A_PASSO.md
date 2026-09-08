# Resolução guiada passo a passo — Worker transfer

Edite `starter/main.mjs` e `starter/worker.mjs`.

### TODO D6-NODE-WORKER
Crie Worker com URL do módulo:
```js
const worker=new Worker(new URL("./worker.mjs", import.meta.url), {type:"module"});
```

### TODO D6-NODE-TRANSFER
Crie `ArrayBuffer(1024)`, preencha `Uint8Array`. Guarde expected sum. Envie:
```js
worker.postMessage(buffer,[buffer]);
```
Imediatamente depois, `buffer.byteLength` deve ser 0.

### TODO D6-NODE-RECEIVE
No worker:
```js
parentPort.on("message",(buffer)=>{
 const bytes=new Uint8Array(buffer);
 let sum=0; for(const b of bytes) sum+=b;
 parentPort.postMessage({sum,length:bytes.length});
});
```
No main aguarde message e terminate. O teste executa `runTransfer()` e valida soma, length e detached.
Execute `node starter/test.mjs`.
