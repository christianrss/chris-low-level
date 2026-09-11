'use strict';
const assert = require('assert');
const { createStore, runWith, currentId } = require('./async_context');
// PEDAGOGY-TEST: D7-NODE-ALS
const store = createStore();
assert.ok(store);
// PEDAGOGY-TEST: D7-NODE-RUN
// PEDAGOGY-TEST: D7-NODE-GET
runWith(store, 7, () => {
  assert.strictEqual(currentId(store), 7);
});
assert.strictEqual(currentId(store), null);
console.log('ok');
