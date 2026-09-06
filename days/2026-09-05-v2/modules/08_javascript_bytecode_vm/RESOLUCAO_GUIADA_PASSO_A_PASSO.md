## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| — | — |

# Resolução guiada passo a passo

Abra `starter/vm.js`, método `run`.

Para `JZ` (`JSVM-JZ-01`):
```js
const cond = this.stack.pop();
if (cond === 0) this.ip = ins.arg;
else this.ip++;
```

Para `JMP` (`JSVM-JMP-02`):
```js
this.ip = ins.arg;
```

Não incremente `ip` novamente depois de definir o target. Rode `node starter/test.js`. Se falhar, adicione temporariamente `console.log({ip:this.ip, ins, stack:[...this.stack]})`. Remova o trace ao terminar.

## Mapa de consistência auditada
- `JSVM-JZ-01` - starter -> resolução -> teste -> solution.
- `JSVM-JMP-02` - starter -> resolução -> teste -> solution.
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

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.


## `JS-VM-DISPATCH-01`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/vm.js` |
| **Função / âncora** | `TODO [JS-VM-DISPATCH-01]` |
| **Substituir** | stub marcado por esse TODO |
| **Não mexer** | outros arquivos até este ID passar |

### Escreva o código

```text
# Implemente conforme starter/vm.js e compare solutions/vm.js
```

### Por que funciona

A edição no arquivo certo faz o `PEDAGOGY-TEST: JS-VM-DISPATCH-01` passar.
