// TODO [JS-VM-DISPATCH-01]: implement JZ/JMP dispatch
export class VM {
  constructor() {
    this.stack = [];
    this.ip = 0;
  }
  run(p) {
    this.ip = 0;
    this.stack = [];
    let steps = 0;
    while (this.ip < p.length) {
      if (++steps > 1000) throw new Error("step limit");
      const ins = p[this.ip];
      switch (ins.op) {
        case "PUSH":
          this.stack.push(ins.arg);
          this.ip++;
          break;
        case "JZ":
          // TODO [JS-VM-DISPATCH-01]
          this.ip++;
          break;
        case "JMP":
          // TODO [JS-VM-DISPATCH-01]
          this.ip++;
          break;
        case "HALT":
          return this.stack;
        default:
          throw new Error("bad op");
      }
    }
    return this.stack;
  }
}
