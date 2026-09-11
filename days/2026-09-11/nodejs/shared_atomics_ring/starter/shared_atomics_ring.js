export const CAP = 4;
export class AtomicsRing {
  constructor(sab) {
    this.view = new Int32Array(sab);
    // layout: [head, tail, slot0, slot1, slot2, slot3]  — 6 int32
  }
  push(v) {
    // TODO [NODE-RING-01]: push if not full; return false if full
    void v; return false;
  }
  pop() {
    // TODO [NODE-RING-02]: pop or null if empty
    return null;
  }
  size() {
    // TODO [NODE-RING-03]: (tail-head+CAP*2)%(CAP*2) style count of items
    return -1;
  }
}
export function makeSab() {
  return new SharedArrayBuffer(6 * 4);
}
