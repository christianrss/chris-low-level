import {runTransfer} from "./main.mjs";
// PEDAGOGY-TEST: D6-NODE-WORKER
// PEDAGOGY-TEST: D6-NODE-TRANSFER
// PEDAGOGY-TEST: D6-NODE-RECEIVE
const r=await runTransfer(); if(r.length!==1024||!r.detached||r.sum<=0) throw new Error(JSON.stringify(r));
console.log("chris-worker-transfer tests passed");
