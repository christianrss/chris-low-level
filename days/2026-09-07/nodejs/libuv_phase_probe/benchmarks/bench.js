import {boundedNextTick} from "../solutions/probe.js";
const samples=[];
for(let r=0;r<30;r++){const t=process.hrtime.bigint();await boundedNextTick(10000);samples.push(Number(process.hrtime.bigint()-t)/1e6);}
samples.sort((a,b)=>a-b);console.log(`10000_nextTicks median_ms=${samples[15].toFixed(3)} min=${samples[0].toFixed(3)} max=${samples.at(-1).toFixed(3)}`);
