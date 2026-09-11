'use strict';
const { AsyncLocalStorage } = require('async_hooks');

function createStore() {
  // TODO [D7-NODE-ALS]
  throw new Error('D7-NODE-ALS');
}

function runWith(store, id, fn) {
  // TODO [D7-NODE-RUN]
  throw new Error('D7-NODE-RUN');
}

function currentId(store) {
  // TODO [D7-NODE-GET]
  throw new Error('D7-NODE-GET');
}

module.exports = { createStore, runWith, currentId };
