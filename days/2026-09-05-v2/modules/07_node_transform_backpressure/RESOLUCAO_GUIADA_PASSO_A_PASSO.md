## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| `NODE-BACKPRESSURE-02` | `starter/backpressure_demo.js` |

# Resolução guiada passo a passo

Abra `starter/line_transform.js`. Em `_transform`, use `this.decoder.write(chunk)`, concatene com `this.pending`, faça `split('\n')`, guarde o último item em pending e faça `push()` nas linhas completas. Em `_flush`, combine `this.pending + this.decoder.end()` e envie o resto se não vazio. Isso fecha `NODE-XFORM-01`.

Agora abra o arquivo real `starter/backpressure_demo.js`. No bloco `if (!ok)`, incremente o contador e adicione:
```js
await once(sink, 'drain');
```
Na solution também contamos `drains` e exigimos `drains === falseWrites`. Isso fecha `NODE-BACKPRESSURE-02`.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/backpressure_demo.js` |
| **Função / âncora** | comentário `TODO [NODE-BACKPRESSURE-02]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [NODE-BACKPRESSURE-02]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |

Teste:
```bash
node starter/test.js
node starter/backpressure_demo.js
```

Se o teste de UTF-8 falhar, verifique se a divisão acontece antes/depois do decoder. Se backpressure não aparecer, reduza `highWaterMark`.

## Mapa de consistência auditada
- `NODE-XFORM-01` - starter -> resolução -> teste -> solution.
- `NODE-BACKPRESSURE-02` - starter -> resolução -> teste -> solution.
## Relatório de resolução

- **TODOs concluídos:** (liste os IDs implementados)
- **Comandos de teste:**
  ```bash
  # cole aqui o comando exato usado
  ```
- **Saída esperada:** PASS nos testes do módulo
- **Invariantes verificadas:** (liste)
- **Edge cases testados:** (liste)
- **Benchmark:** hipótese + resultado ou declaração honesta de skip
- **Toolchain não executada:** (se aplicável)

### 4. Por que funciona

O stub no âncora TODO é substituído pelo comportamento testado.

### Debug

Use mensagens de assert/teste; compare com `solutions/`.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.


## `NODE-BACKPRESSURE-01`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/backpressure_demo.js` |
| **Função / âncora** | `TODO [NODE-BACKPRESSURE-01]` |
| **Substituir** | stub marcado por esse TODO |
| **Não mexer** | outros arquivos até este ID passar |

### Escreva o código

```text
# Implemente conforme starter/backpressure_demo.js e compare solutions/backpressure_demo.js
```

### Por que funciona

A edição no arquivo certo faz o `PEDAGOGY-TEST: NODE-BACKPRESSURE-01` passar.
