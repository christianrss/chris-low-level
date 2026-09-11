# Resolução guiada — duplex_event_pipe

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `ND-DUPLEX-01` | `starter/duplex_event_pipe.js` | `_write` | corpo sob `TODO [ND-DUPLEX-01]` | assinaturas e testes |
| `ND-DUPLEX-02` | `starter/duplex_event_pipe.js` | `_read` | corpo sob `TODO [ND-DUPLEX-02]` | assinaturas e testes |
| `ND-DUPLEX-03` | `starter/duplex_event_pipe.js` | `metrics` | corpo sob `TODO [ND-DUPLEX-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/nodejs/duplex_event_pipe/starter
node test.js
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## ND-DUPLEX-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/duplex_event_pipe.js` |
| Função / âncora | `_write` / comentário `TODO [ND-DUPLEX-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem _write framing, 48 bytes ≠ 2 eventos.

### Algoritmo / trace

concat; slice de 24; incremente eventsWritten; chame _read.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```javascript
_write(chunk, encoding, callback) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-01
        this._writeBuf = Buffer.concat([this._writeBuf, chunk]);
        while (this._writeBuf.length >= EVENT_SIZE) {
            const ev = this._writeBuf.subarray(0, EVENT_SIZE);
            this._writeBuf = this._writeBuf.subarray(EVENT_SIZE);
            this._readBuf = Buffer.concat([this._readBuf, ev]);
            this.eventsWritten++;
        }
        this._read(EVENT_SIZE);
        callback();
    }
```

### Por que funciona?

A rotina `_write` materializa o contrato de `ND-DUPLEX-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `ND-DUPLEX-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `ND-DUPLEX-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## ND-DUPLEX-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/duplex_event_pipe.js` |
| Função / âncora | `_read` / comentário `TODO [ND-DUPLEX-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem _read, o peer não recebe 24-byte frames.

### Algoritmo / trace

push eventos de 24; eventsRead++; break se !push.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```javascript
_read(size) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-02
        while (this._readBuf.length >= EVENT_SIZE) {
            const ev = this._readBuf.subarray(0, EVENT_SIZE);
            this._readBuf = this._readBuf.subarray(EVENT_SIZE);
            this.eventsRead++;
            if (!this.push(ev)) break;
        }
    }
```

### Por que funciona?

A rotina `_read` materializa o contrato de `ND-DUPLEX-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `ND-DUPLEX-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `ND-DUPLEX-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## ND-DUPLEX-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/duplex_event_pipe.js` |
| Função / âncora | `metrics` / comentário `TODO [ND-DUPLEX-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem metrics, o assert de contagem falha.

### Algoritmo / trace

retorne contadores.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```javascript
metrics() {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-03
        return { eventsWritten: this.eventsWritten, eventsRead: this.eventsRead };
    }
```

### Por que funciona?

A rotina `metrics` materializa o contrato de `ND-DUPLEX-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `ND-DUPLEX-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `ND-DUPLEX-03` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| FAIL no Caso 1 | stub intacto / endian errado | releia o trace da TEORIA e o bloco do primeiro TODO |
| PASS parcial | size/estado desalinhado no TODO do meio | imprima pc/head/estado antes do assert |
| Crash / panic | bounds | valide Length/len antes de indexar |
| Diff de string | snprintf/format | compare caractere a caractere com o esperado |

## Relatório de resolução

| TODO | Horas | Maior bug | O que aprendia de novo |
|------|-------|-----------|------------------------|
| `ND-DUPLEX-01` |  |  |  |
| `ND-DUPLEX-02` |  |  |  |
| `ND-DUPLEX-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
