import {parentPort} from "node:worker_threads";
// PEDAGOGY-SOLUTION: D6-NODE-RECEIVE
parentPort.on("message",(buffer)=>{const bytes=new Uint8Array(buffer);let sum=0;for(const b of bytes)sum+=b;parentPort.postMessage({sum,length:bytes.length});});
