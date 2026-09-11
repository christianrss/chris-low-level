'use strict';
const assert = require('assert');
const { createPair, request, serve } = require('./rpc');
(async () => {
  // PEDAGOGY-TEST: D8-NODE-PAIR
  // PEDAGOGY-TEST: D8-NODE-SERVE
  // PEDAGOGY-TEST: D8-NODE-REQ
  const { client, server } = createPair();
  serve(server, { add: (a, b) => a + b });
  const r = await request(client, 'add', [2, 3]);
  assert.strictEqual(r, 5);
  console.log('ok');
  client.close(); server.close();
})();
