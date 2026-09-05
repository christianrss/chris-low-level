// SOLVES [JSVM-JZ-01]
// SOLVES [JSVM-JMP-02]
export class VM{constructor(){this.stack=[];this.ip=0;} run(code){this.ip=0;this.stack=[];while(this.ip<code.length){const ins=code[this.ip];switch(ins.op){case'PUSH':this.stack.push(ins.arg);this.ip++;break;case'JZ':{const c=this.stack.pop();if(c===0)this.ip=ins.arg;else this.ip++;break;}case'JMP':this.ip=ins.arg;break;case'HALT':return this.stack.at(-1);default:throw new Error('bad op');}} return this.stack.at(-1);}}
