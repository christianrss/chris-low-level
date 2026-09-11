# Resolução guiada — shared_atomics_ring

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `NODE-RING-01` | `starter/shared_atomics_ring.js` | `push` |
| `NODE-RING-02` | `starter/shared_atomics_ring.js` | `pop` |
| `NODE-RING-03` | `starter/shared_atomics_ring.js` | `size` |

## Baseline

```powershell
// contexto: substitua o corpo sob o TODO
node days/2026-09-11/nodejs/shared_atomics_ring/starter/test.js
// fim do corpo; preserve a assinatura
```

**Esperado:** FAIL.

## NODE-RING-01

### Onde colocar (NODE-RING-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/shared_atomics_ring.js` |
| Função | `push` |
| Substituir | o corpo sob o comentário `TODO [NODE-RING-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

5º push deve falhar.

### Algoritmo / trace

se tail-head>=CAP false; senão store slot e tail++.

### Escreva o código

```js
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (tail - head >= CAP) return false;
    const slot = 2 + (tail % CAP);
    Atomics.store(this.view, slot, v | 0);
    Atomics.store(this.view, 1, tail + 1);
    return true;
```

### Por que funciona?

Cheio quando 4 itens vivos.

### Verifique

4 ok, 5º false.

### Código completo alinhado ao solutions/ (NODE-RING-01)

```javascript
PEDAGOGY-SOLUTION: NODE-RING-01
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (tail - head >= CAP) return false;
    const slot = 2 + (tail % CAP);
    Atomics.store(this.view, slot, v | 0);
    Atomics.store(this.view, 1, tail + 1);
    return true;
  }
  pop() {
    // 
```

## NODE-RING-02

### Onde colocar (NODE-RING-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/shared_atomics_ring.js` |
| Função | `pop` |
| Substituir | o corpo sob o comentário `TODO [NODE-RING-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

FIFO: 10 depois 20.

### Algoritmo / trace

se head==tail null; senão load e head++.

### Escreva o código

```js
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (head === tail) return null;
    const slot = 2 + (head % CAP);
    const v = Atomics.load(this.view, slot);
    Atomics.store(this.view, 0, head + 1);
    return v;
```

### Por que funciona?

Consome do head.

### Verifique

pop===10 depois 20.

### Código completo alinhado ao solutions/ (NODE-RING-02)

```javascript
PEDAGOGY-SOLUTION: NODE-RING-02
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (head === tail) return null;
    const slot = 2 + (head % CAP);
    const v = Atomics.load(this.view, slot);
    Atomics.store(this.view, 0, head + 1);
    return v;
  }
  size() {
    // 
```

## NODE-RING-03

### Onde colocar (NODE-RING-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/shared_atomics_ring.js` |
| Função | `size` |
| Substituir | o corpo sob o comentário `TODO [NODE-RING-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

size após 4 pushes = 4.

### Algoritmo / trace

tail - head.

### Escreva o código

```js
    return Atomics.load(this.view, 1) - Atomics.load(this.view, 0);
    // size
    // end
```

### Por que funciona?

Itens vivos = diferença dos cursores.

### Verifique

size===4 e depois 2.

### Código completo alinhado ao solutions/ (NODE-RING-03)

```javascript
PEDAGOGY-SOLUTION: NODE-RING-03
    return Atomics.load(this.view, 1) - Atomics.load(this.view, 0);
  }
}
export function makeSab() {
  return new SharedArrayBuffer(6 * 4);
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| slot errado | 2+(i%CAP) |

## Relatório de resolução

- TODOs: [ ]
