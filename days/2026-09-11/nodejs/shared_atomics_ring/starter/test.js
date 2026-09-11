import { AtomicsRing, makeSab, CAP } from "./shared_atomics_ring.js";
function assert(c, m) { if (!c) { console.error("FAIL", m); process.exit(1); } }
const r = new AtomicsRing(makeSab());
// PEDAGOGY-TEST: NODE-RING-01
assert(r.push(10) === true, "p1");
assert(r.push(20) === true, "p2");
assert(r.push(30) === true, "p3");
assert(r.push(40) === true, "p4");
assert(r.push(50) === false, "full");
// PEDAGOGY-TEST: NODE-RING-03
assert(r.size() === 4, "size4");
// PEDAGOGY-TEST: NODE-RING-02
assert(r.pop() === 10, "pop10");
assert(r.pop() === 20, "pop20");
assert(r.size() === 2, "size2");
assert(CAP === 4, "cap");
console.log("ok");
