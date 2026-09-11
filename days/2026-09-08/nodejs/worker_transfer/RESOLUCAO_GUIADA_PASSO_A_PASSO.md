# Resolucao guiada — worker_transfer

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-NODE-WORKER` | `starter/main.mjs` | `function` |
| `D6-NODE-TRANSFER` | `starter/main.mjs` | `function` |
| `D6-NODE-RECEIVE` | `starter/worker.mjs` | `?` |


## Baseline

```powershell
cd days/2026-09-08/nodejs/worker_transfer/starter
node test.mjs
```

**Esperado antes dos TODOs:** FAIL.


## D6-NODE-WORKER

### Onde colocar (D6-NODE-WORKER)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/main.mjs` |
| Funcao | `function` |
| Substituir | corpo sob `TODO [D6-NODE-WORKER]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-NODE-WORKER` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-NODE-WORKER` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```javascript
PEDAGOGY-SOLUTION: D6-NODE-WORKER
  const worker=new Worker(new URL("./worker.mjs",import.meta.url),{type:"module"});
  const buffer=new ArrayBuffer(1024); const bytes=new Uint8Array(buffer); let expected=0;
  for(let i=0;i<bytes.length;i++){bytes[i]=i%251;expected+=bytes[i];}
  // 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-NODE-WORKER`.

### Verifique
Rode o baseline; o caminho de `D6-NODE-WORKER` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-NODE-WORKER` PASS
- [ ] Nao alterei o teste

## D6-NODE-TRANSFER

### Onde colocar (D6-NODE-TRANSFER)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/main.mjs` |
| Funcao | `function` |
| Substituir | corpo sob `TODO [D6-NODE-TRANSFER]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-NODE-TRANSFER` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-NODE-TRANSFER` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```javascript
PEDAGOGY-SOLUTION: D6-NODE-TRANSFER
  const resultP=new Promise((resolve,reject)=>{worker.once("message",resolve);worker.once("error",reject);});
  worker.postMessage(buffer,[buffer]); const detached=buffer.byteLength===0;
  const result=await resultP; await worker.terminate();
  if(result.sum!==expected) throw new Error("checksum mismatch");
  return {...result,detached};
}
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-NODE-TRANSFER`.

### Verifique
Rode o baseline; o caminho de `D6-NODE-TRANSFER` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-NODE-TRANSFER` PASS
- [ ] Nao alterei o teste

## D6-NODE-RECEIVE

### Onde colocar (D6-NODE-RECEIVE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/worker.mjs` |
| Funcao | `?` |
| Substituir | corpo sob `TODO [D6-NODE-RECEIVE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-NODE-RECEIVE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-NODE-RECEIVE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```javascript
// PEDAGOGY-SOLUTION: D6-NODE-RECEIVE
parentPort.on("message", (buffer) => {
  const bytes = new Uint8Array(buffer);
  let sum = 0;
  for (const b of bytes) sum += b;
  parentPort.postMessage({ sum, length: bytes.length });
});
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-NODE-RECEIVE`.

### Verifique
Rode o baseline; o caminho de `D6-NODE-RECEIVE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-NODE-RECEIVE` PASS
- [ ] Nao alterei o teste

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco do TODO |
| off-by-one | size/indice | refaca o trace |
| 2o caso falha | estado residual | reset |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado / preencher
