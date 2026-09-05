// PEDAGOGY-SOLUTION: JSVM-JZ-01
// PEDAGOGY-SOLUTION: JSVM-JMP-02
export class VM {
    constructor() {
        this.stack = [];
        this.ip = 0;
        this.trace = [];
    }

    _jumpTarget(program, target) {
        if (!Number.isInteger(target) || target < 0 || target >= program.length) {
            throw new Error('bad target');
        }
        return target;
    }

    run(program) {
        this.ip = 0;
        this.stack = [];
        this.trace = [];
        let steps = 0;

        while (this.ip < program.length) {
            if (++steps > 1000) {
                throw new Error('step limit');
            }

            const instruction = program[this.ip];
            this.trace.push(this.ip);

            switch (instruction.op) {
            case 'PUSH':
                this.stack.push(instruction.arg);
                this.ip++;
                break;
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
            case 'JMP':
                this.ip = this._jumpTarget(program, instruction.arg);
                break;
            case 'HALT':
                return this.stack.at(-1);
            default:
                throw new Error('bad op');
            }
        }

        return this.stack.at(-1);
    }
}
