// PEDAGOGY-TEST [JSVM-JZ-01]: ramo falso salta para PUSH 20
// PEDAGOGY-TEST [JSVM-JMP-02]: ramo verdadeiro executa PUSH 10 e trace de IP
import assert from 'node:assert/strict';
import { VM } from './vm.js';

const makeProgram = (condition) => [
    { op: 'PUSH', arg: condition },
    { op: 'JZ', arg: 4 },
    { op: 'PUSH', arg: 10 },
    { op: 'JMP', arg: 5 },
    { op: 'PUSH', arg: 20 },
    { op: 'HALT' },
];

const vm = new VM();
assert.equal(vm.run(makeProgram(0)), 20);
assert.deepEqual(vm.trace, [0, 1, 4, 5]);

assert.equal(vm.run(makeProgram(1)), 10);
assert.deepEqual(vm.trace, [0, 1, 2, 3, 5]);

console.log('OK jsvm branches');
