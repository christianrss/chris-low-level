# Resolução guiada — input_event_transform

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função | Substituir |
|---------|-----------------|--------|------------|
| `ND-INPUT-01` | `starter/input_event_transform.js` | `_transform` | stub TODO |
| `ND-INPUT-02` | `starter/input_event_transform.js` | `_flush` | stub TODO |
| `ND-INPUT-03` | `starter/input_event_transform.js` | `metrics` | stub TODO |

## Baseline

```powershell
cd days/2026-09-07/nodejs/input_event_transform/starter
node test.js
```

**Esperado:** FAIL até parse de eventos 24B.

## Relatório de resolução

## ND-INPUT-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/input_event_transform.js` |
| Função | `_transform` |

### 1. O problema

Chunks TCP/pipe podem cortar eventos de 24 bytes — buffer obrigatório.

### Escreva o código

```javascript
_transform(chunk, encoding, callback) {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    while (this.buffer.length >= EVENT_SIZE) {
        const ev = this.buffer.subarray(0, EVENT_SIZE);
        this.buffer = this.buffer.subarray(EVENT_SIZE);
        this.eventsParsed++;
        this.push({ raw: Buffer.from(ev) });
    }
    callback();
}
```

### Por que funciona?

Loop extrai registros completos antes de emitir downstream.

### Verifique

Caso 1: buffer 48B → dois objetos `{raw}`.

### Debug

| Sintoma | Ação |
|---------|------|
| 0 eventos | verificar concat do buffer |

---

## ND-INPUT-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/input_event_transform.js` |
| Função | `_flush` |

### 1. O problema

Bytes residuais violam contrato evdev de registro fixo.

### Escreva o código

```javascript
_flush(callback) {
    if (this.buffer.length > 0) {
        callback(new Error('trailing partial event'));
        return;
    }
    callback();
}
```

### Por que funciona?

Flush só é válido com buffer vazio quando registros são fixos.

### Verifique

Caso 2: 1 byte sobrando → erro no flush.

---

## ND-INPUT-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/input_event_transform.js` |
| Função | `metrics` |

### 1. O problema

Observabilidade espelha `gunzip_transform` (Day 06).

### Escreva o código

```javascript
metrics() {
    return {
        eventsParsed: this.eventsParsed,
        backpressurePauses: this.backpressurePauses,
    };
}
```

### Por que funciona?

Contadores expõem throughput e backpressure sem debugger.

### Verifique

Caso 3: após dois eventos, `eventsParsed === 2`.

### Resultado esperado

`node test.js` imprime `OK input_event_transform`.
