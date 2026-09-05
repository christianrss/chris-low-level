# Resolução guiada passo a passo — JavaScript — Bytecode Branch VM

## Mapa exato starter → resolução

- `JSVM-JZ-01` → `starter/vm.js` (case `JZ` em `run`)
- `JSVM-JMP-02` → `starter/vm.js` (case `JMP` em `run`)

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/javascript/bytecode_branch_vm/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

Na raiz do repositório:

```bash
cd days/2026-09-05/javascript/bytecode_branch_vm/starter
npm test
```

O comando deve executar, mas os testes **devem falhar**: com `condition=0`, a VM retorna `undefined` (não executa `PUSH 20`); com `condition=1`, o trace não inclui o salto via `JMP`. Esse é o baseline.

## `JSVM-JZ-01` — desvio se topo da pilha == 0

### Arquivo

Abra:

```text
starter/vm.js
```

Localize o case `JZ`:

```javascript
case 'JZ':
    // TODO [JSVM-JZ-01]: desvia se topo da pilha == 0
    this.ip++;
    break;
```

Substitua por:

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

### Por que funciona?

`PUSH` deixa o valor condicional no topo. `pop()` remove e testa com `=== 0`. Se zero, `ip` vai para o índice 4 (`PUSH 20`); se não, avança para `ip=2` (`PUSH 10`).

### Verificação manual

Com `condition=0`:

```text
ip=0 PUSH 0
ip=1 JZ→4  (pop 0, salta)
ip=4 PUSH 20
ip=5 HALT  → retorna 20
trace: [0, 1, 4, 5]
```

### Checkpoint

```bash
npm test
```

O primeiro par de asserts (`run(0) === 20` e trace `[0,1,4,5]`) deve passar; o segundo par ainda falha até implementar `JMP`.

---

## `JSVM-JMP-02` — salto incondicional

### Arquivo

Localize o case `JMP`:

```javascript
case 'JMP':
    // TODO [JSVM-JMP-02]: salto incondicional
    this.ip++;
    break;
```

Substitua por:

```javascript
case 'JMP':
    this.ip = this._jumpTarget(program, instruction.arg);
    break;
```

### Por que funciona?

Após `PUSH 10` em `ip=2`, o programa em `ip=3` deve pular o `PUSH 20` em `ip=4` e ir direto para `HALT` em `ip=5`. `_jumpTarget` valida que `5` está dentro dos limites.

### Verificação manual

Com `condition=1`:

```text
ip=0 PUSH 1
ip=1 JZ      (pop 1, ip→2)
ip=2 PUSH 10
ip=3 JMP→5  (pula índice 4)
ip=5 HALT   → retorna 10
trace: [0, 1, 2, 3, 5]
```

### Checkpoint

Todos os asserts passam.

---

## Rode os testes novamente

```bash
npm test
```

Saída esperada contém:

```text
OK jsvm branches
```

## Como depurar se falhar

- Retorno `undefined` com `condition=0`: `JZ` não salta — ainda faz `ip++` fixo.
- Retorno `20` com `condition=1`: falta `JMP` — executou `PUSH 20` indevidamente.
- Trace com `4` quando deveria pular: `JMP` não atribui `ip` diretamente.
- `bad target`: `instruction.arg` fora de `[0, length)` — confira o programa em `test.js`.
- `underflow`: `JZ` sem `PUSH` anterior.

Inspeção rápida:

```javascript
const vm = new VM();
console.log(vm.run(makeProgram(0)));
console.log(vm.trace);
```

## Solução final comentada

Compare `starter/vm.js` com `solutions/vm.js`. Justifique: consumo da pilha em `JZ`, diferença entre salto condicional e incondicional, e uso de `_jumpTarget`.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| JSVM-JZ-01 | `vm.js` | `condition=0` → resultado 20; trace `[0,1,4,5]` |
| JSVM-JMP-02 | `vm.js` | `condition=1` → resultado 10; trace `[0,1,2,3,5]` |

Critério de aceite: `npm test` imprime `OK jsvm branches` sem falha.

### Template do relatório

```
Aluno:
Módulo: JavaScript — Bytecode Branch VM
Data:

1. TODOs: JSVM-JZ-01, JSVM-JMP-02
2. Primeira falha: [ex.: expected 20, got undefined]
3. Correção aplicada: [ex.: pop + ip condicional em JZ; JMP com _jumpTarget]
4. Evidência: [colar saída OK jsvm branches]
```
