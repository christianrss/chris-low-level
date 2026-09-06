# RESOLUÇÃO GUIADA — JavaScript / Bytecode branch VM

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `JSVM-JZ-01` | `starter/vm.js` | `run` — case `JZ` (pop + salto se 0) |
| `JSVM-JMP-02` | `starter/vm.js` | `run` — case `JMP` (salto absoluto) |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test.js`.

> Trabalhe em `days/2026-09-05/javascript/bytecode_branch_vm/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Rode `npm test` / `node test.js` após cada case.

---

## JSVM-JZ-01 — salto condicional

### 1. O problema (starter stub)

```javascript
case 'JZ':
    // TODO [JSVM-JZ-01]: desvia se topo da pilha == 0
    this.ip++;
    break;
```

Programa do teste (`makeProgram(condition)`):

```text
0 PUSH condition
1 JZ  → 4
2 PUSH 10
3 JMP → 5
4 PUSH 20
5 HALT
```

Com `JZ` = só `ip++`, `condition=0` nunca alcança `PUSH 20` via salto → retorno `undefined` (cai em `PUSH 10`/`JMP` stub).

### 2. O algoritmo

```text
condition ← stack.pop()
se condition === undefined → Error('underflow')
se condition === 0:
  ip ← _jumpTarget(program, instruction.arg)
senão:
  ip ← ip + 1
```

`_jumpTarget` já valida `arg ∈ [0, program.length)`.

### 3. Código completo

Substitua o case `JZ` em `starter/vm.js`:

```javascript
case 'JZ': {
    const condition = this.stack.pop();
    if (condition === undefined) {
        throw new Error('underflow');
    }
    this.ip = condition === 0
        ? this._jumpTarget(program, instruction.arg)
        : this.ip + 1;
    break;
}
```

### 4. Por que funciona?

- `PUSH` deixa o predicado no topo; `JZ` **consome** (como VM de pilha real) — não deixa valor residual.
- `=== 0`: só zero desvia; `1` (e qualquer não-zero) cai no ramo then (`PUSH 10`).
- Não fazer `ip++` depois do salto: `_jumpTarget` já define o próximo IP absoluto.
- `underflow`: `JZ` sem `PUSH` é bug de programa — falha explícita.

### 5. Verificação parcial

Trace com `condition=0`:

```text
ip=0 PUSH 0     stack=[0]     trace+[0]
ip=1 JZ→4       stack=[]      trace+[1]
ip=4 PUSH 20    stack=[20]    trace+[4]
ip=5 HALT → 20                trace+[5]
trace = [0, 1, 4, 5]
```

```bash
cd days/2026-09-05/javascript/bytecode_branch_vm/starter
node test.js
```

Esperado: primeiro assert (`run(0)===20`, trace) passa; segundo ainda falha até `JMP`.

---

## JSVM-JMP-02 — salto incondicional

### 1. O problema (starter stub)

```javascript
case 'JMP':
    // TODO [JSVM-JMP-02]: salto incondicional
    this.ip++;
    break;
```

Com `condition=1`, o fluxo chega em `PUSH 10` e depois precisa pular o `PUSH 20`. Stub `ip++` executa o índice 4 → retorno 20 em vez de 10; trace inclui `4`.

### 2. O algoritmo

```text
ip ← _jumpTarget(program, instruction.arg)
```

Sem pop; sem `ip++` extra.

### 3. Código completo

```javascript
case 'JMP':
    this.ip = this._jumpTarget(program, instruction.arg);
    break;
```

### 4. Por que funciona?

- Salto absoluto para o índice do argumento (`5` = `HALT`), validado por `_jumpTarget`.
- Sem consumir pilha: `JMP` não é condicional.
- Evita executar `PUSH 20` no ramo verdadeiro — o `JZ` já escolheu o caminho then.

### 5. Verificação

Trace com `condition=1`:

```text
ip=0 PUSH 1     stack=[1]     trace+[0]
ip=1 JZ (≠0)    stack=[]      ip→2   trace+[1]
ip=2 PUSH 10    stack=[10]    trace+[2]
ip=3 JMP→5                    trace+[3]
ip=5 HALT → 10                trace+[5]
trace = [0, 1, 2, 3, 5]
```

```bash
node test.js
```

Saída esperada:

```text
OK jsvm branches
```

Debug: retorno `20` com condition 1 → `JMP` ainda faz `ip++`; `bad target` → `arg` fora do range; `step limit` → loop infinito (salto para si mesmo sem HALT).

Inspeção rápida:

```javascript
import { VM } from './vm.js';
const vm = new VM();
console.log(vm.run([{op:'PUSH',arg:0},{op:'JZ',arg:4},{op:'PUSH',arg:10},{op:'JMP',arg:5},{op:'PUSH',arg:20},{op:'HALT'}]));
console.log(vm.trace);
```

---

## Mapa de consistência auditada

- `JSVM-JZ-01` — `starter/vm.js` → `solutions/vm.js` (case `JZ`).
- `JSVM-JMP-02` — `starter/vm.js` → `solutions/vm.js` (case `JMP`).

## Relatório de resolução

### O que foi validado

- TODOs `JSVM-JZ-01` e `JSVM-JMP-02` nos cases de `VM.run`.
- `PEDAGOGY-TEST` em `test.js`: resultado 20/10 e traces `[0,1,4,5]` / `[0,1,2,3,5]`.
- Starter com `ip++` fixo falha ambos os ramos até os saltos corretos.

### Armadilhas encontradas

- `JZ` sem `pop` (ou peek sem consumir) deixa lixo na pilha.
- Fazer `ip++` depois de atribuir o alvo do salto.
- Comparar com `==` frouxo ou tratar só `false` em vez de `=== 0`.

### Depuração e saída esperada

- **Depuração:** logue `ip`, `instruction.op`, `stack` a cada passo; compare com o trace esperado.
- **Saída esperada:** `OK jsvm branches`.

### Próximo passo sugerido

Refazer JZ/JMP sem a resolução. Meça passos até HALT em loops em `BENCHMARK_GUIADO.md` (respeitando o step limit 1000).
