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
