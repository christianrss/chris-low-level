// TESTS [JSVM-JZ-01] [JSVM-JMP-02]
import assert from 'node:assert/strict';import {VM} from './vm.js';const vm=new VM();const p=[{op:'PUSH',arg:0},{op:'JZ',arg:4},{op:'PUSH',arg:10},{op:'JMP',arg:5},{op:'PUSH',arg:20},{op:'HALT'}];assert.deepEqual(vm.run(p),[20]);assert.throws(()=>vm.run([{op:'JMP',arg:99}]));console.log('OK JS VM');
