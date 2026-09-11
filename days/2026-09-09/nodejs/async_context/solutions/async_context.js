'use strict';
const { AsyncLocalStorage } = require('async_hooks');

function createStore() {
  // PEDAGOGY-SOLUTION: D7-NODE-ALS
  return new AsyncLocalStorage();
}

function runWith(store, id, fn) {
  // PEDAGOGY-SOLUTION: D7-NODE-RUN
  return store.run({ id }, fn);
}

function currentId(store) {
  // PEDAGOGY-SOLUTION: D7-NODE-GET
  const s = store.getStore();
  return s ? s.id : null;
}

module.exports = { createStore, runWith, currentId };
