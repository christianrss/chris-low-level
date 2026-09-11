import {Worker} from "node:worker_threads";
export async function runTransfer(){
  // PEDAGOGY-SOLUTION: D6-NODE-WORKER
  const worker=new Worker(new URL("./worker.mjs",import.meta.url),{type:"module"});
  const buffer=new ArrayBuffer(1024); const bytes=new Uint8Array(buffer); let expected=0;
  for(let i=0;i<bytes.length;i++){bytes[i]=i%251;expected+=bytes[i];}
  // PEDAGOGY-SOLUTION: D6-NODE-TRANSFER
  const resultP=new Promise((resolve,reject)=>{worker.once("message",resolve);worker.once("error",reject);});
  worker.postMessage(buffer,[buffer]); const detached=buffer.byteLength===0;
  const result=await resultP; await worker.terminate();
  if(result.sum!==expected) throw new Error("checksum mismatch");
  return {...result,detached};
}
