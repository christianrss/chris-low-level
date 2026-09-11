export const CAP = 4;
export class AtomicsRing {
  constructor(sab) {
    this.view = new Int32Array(sab);
  }
  push(v) {
    // PEDAGOGY-SOLUTION: NODE-RING-01
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (tail - head >= CAP) return false;
    const slot = 2 + (tail % CAP);
    Atomics.store(this.view, slot, v | 0);
    Atomics.store(this.view, 1, tail + 1);
    return true;
  }
  pop() {
    // PEDAGOGY-SOLUTION: NODE-RING-02
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (head === tail) return null;
    const slot = 2 + (head % CAP);
    const v = Atomics.load(this.view, slot);
    Atomics.store(this.view, 0, head + 1);
    return v;
  }
  size() {
    // PEDAGOGY-SOLUTION: NODE-RING-03
    return Atomics.load(this.view, 1) - Atomics.load(this.view, 0);
  }
}
export function makeSab() {
  return new SharedArrayBuffer(6 * 4);
}
