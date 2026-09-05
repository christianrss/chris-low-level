import assert from 'node:assert/strict'; import {VM} from './vm.js';
const make=(cond)=>[{op:'PUSH',arg:cond},{op:'JZ',arg:4},{op:'PUSH',arg:10},{op:'JMP',arg:5},{op:'PUSH',arg:20},{op:'HALT'}]; const vm=new VM(); assert.equal(vm.run(make(0)),20); assert.equal(vm.run(make(1)),10); console.log('OK jsvm branches');
