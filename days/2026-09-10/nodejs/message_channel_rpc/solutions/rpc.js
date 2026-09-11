'use strict';
const { MessageChannel } = require('worker_threads');
function createPair() {
  // PEDAGOGY-SOLUTION: D8-NODE-PAIR
  const { port1, port2 } = new MessageChannel();
  return { client: port1, server: port2 };
}
function request(port, method, args) {
  // PEDAGOGY-SOLUTION: D8-NODE-REQ
  return new Promise((resolve, reject) => {
    const onMsg = (msg) => {
      port.off('message', onMsg);
      if (msg.error) reject(new Error(msg.error));
      else resolve(msg.result);
    };
    port.on('message', onMsg);
    port.postMessage({ method, args });
  });
}
function serve(port, handlers) {
  // PEDAGOGY-SOLUTION: D8-NODE-SERVE
  port.on('message', (msg) => {
    try {
      const fn = handlers[msg.method];
      if (!fn) throw new Error('unknown');
      const result = fn(...(msg.args || []));
      port.postMessage({ result });
    } catch (e) {
      port.postMessage({ error: String(e.message || e) });
    }
  });
}
module.exports = { createPair, request, serve };
