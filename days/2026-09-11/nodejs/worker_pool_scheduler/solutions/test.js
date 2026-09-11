'use strict';
const assert = require('assert');
const { createPool, submit, shutdown } = require('./pool');
(async () => {
  // PEDAGOGY-TEST: D9-NODE-POOL
  // PEDAGOGY-TEST: D9-NODE-SUBMIT
  // PEDAGOGY-TEST: D9-NODE-SHUT
  const p = createPool(2);
  const a = await submit(p, async (id) => id);
  assert.strictEqual(a, 1);
  assert.strictEqual(shutdown(p), true);
  console.log('ok');
})();
