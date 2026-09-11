'use strict';
function createPool(size) {
  // PEDAGOGY-SOLUTION: D9-NODE-POOL
  return { size, active: 0, q: [], closed: false, nextId: 1 };
}
function submit(pool, fn) {
  // PEDAGOGY-SOLUTION: D9-NODE-SUBMIT
  if (pool.closed) return Promise.reject(new Error('closed'));
  const id = pool.nextId++;
  return new Promise((resolve, reject) => {
    const job = { id, fn, resolve, reject };
    if (pool.active < pool.size) run(pool, job);
    else pool.q.push(job);
  });
}
function run(pool, job) {
  pool.active++;
  Promise.resolve()
    .then(() => job.fn(job.id))
    .then(
      (value) => {
        pool.active--;
        if (pool.q.length) run(pool, pool.q.shift());
        job.resolve(value);
      },
      (err) => {
        pool.active--;
        if (pool.q.length) run(pool, pool.q.shift());
        job.reject(err);
      }
    );
}
function shutdown(pool) {
  // PEDAGOGY-SOLUTION: D9-NODE-SHUT
  pool.closed = true;
  return pool.active === 0 && pool.q.length === 0;
}
module.exports = { createPool, submit, shutdown };
