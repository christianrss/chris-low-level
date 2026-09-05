# Resolução guiada passo a passo — JavaScript runtime from scratch: branches em bytecode VM

Abra `starter/vm.js`, método `run`.

Para `JZ`:
```js
const cond=this.stack.pop();
if(cond===0) this.ip=ins.arg; else this.ip++;
```
Para `JMP`:
```js
this.ip=ins.arg;
```
Não incremente `ip` depois de sobrescrevê-lo.

O programa de teste representa: `if (0) push 10 else push 20`. Use trace temporário `console.log({ip,ins,stack:[...this.stack]})` para ver o salto.

## Mapa de consistência auditada
- `JSVM-JZ-01` — starter → resolução → teste → solution.
- `JSVM-JMP-02` — starter → resolução → teste → solution.
