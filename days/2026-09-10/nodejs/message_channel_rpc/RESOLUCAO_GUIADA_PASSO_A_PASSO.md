# Resolucao guiada — message_channel_rpc

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-NODE-PAIR` | `starter/rpc.js` | `createPair` |
| `D8-NODE-REQ` | `starter/rpc.js` | `request` |
| `D8-NODE-SERVE` | `starter/rpc.js` | `serve` |


## Baseline

```powershell
cd days/2026-09-10/nodejs/message_channel_rpc/starter
node test.js
```

**Esperado antes dos TODOs:** FAIL.


## D8-NODE-PAIR

### Onde colocar (D8-NODE-PAIR)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/rpc.js` |
| Funcao | `createPair` |
| Substituir | corpo sob `TODO [D8-NODE-PAIR]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-NODE-PAIR` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-NODE-PAIR`.

### Escreva o codigo

```javascript
  const { port1, port2 } = new MessageChannel();
  return { client: port1, server: port2 };
}
function request(port, method, args) {
  return new Promise((resolve, reject) => {
    const onMsg = (msg) => {
      port.off('message', onMsg);
      if (msg.error) reject(new Error(msg.error));
```

### Por que funciona?
Materializa o contrato numerico de `D8-NODE-PAIR`.

### Verifique
Baseline parcial; `D8-NODE-PAIR` PASS.

### Checkpoint
- [ ] `D8-NODE-PAIR` PASS

## D8-NODE-REQ

### Onde colocar (D8-NODE-REQ)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/rpc.js` |
| Funcao | `request` |
| Substituir | corpo sob `TODO [D8-NODE-REQ]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-NODE-REQ` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-NODE-REQ`.

### Escreva o codigo

```javascript
  return new Promise((resolve, reject) => {
    const onMsg = (msg) => {
      port.off('message', onMsg);
      if (msg.error) reject(new Error(msg.error));
      else resolve(msg.result);
    };
    port.on('message', onMsg);
    port.postMessage({ method, args });
```

### Por que funciona?
Materializa o contrato numerico de `D8-NODE-REQ`.

### Verifique
Baseline parcial; `D8-NODE-REQ` PASS.

### Checkpoint
- [ ] `D8-NODE-REQ` PASS

## D8-NODE-SERVE

### Onde colocar (D8-NODE-SERVE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/rpc.js` |
| Funcao | `serve` |
| Substituir | corpo sob `TODO [D8-NODE-SERVE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-NODE-SERVE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-NODE-SERVE`.

### Escreva o codigo

```javascript
  port.on('message', (msg) => {
    try {
      const fn = handlers[msg.method];
      if (!fn) throw new Error('unknown');
      const result = fn(...(msg.args || []));
      port.postMessage({ result });
    } catch (e) {
      port.postMessage({ error: String(e.message || e) });
```

### Por que funciona?
Materializa o contrato numerico de `D8-NODE-SERVE`.

### Verifique
Baseline parcial; `D8-NODE-SERVE` PASS.

### Checkpoint
- [ ] `D8-NODE-SERVE` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco |
| off-by-one | size | refaca trace |

## Relatorio de resolucao

- TODOs:
- Saida:
- Invariantes:
- Benchmark: nao executado
