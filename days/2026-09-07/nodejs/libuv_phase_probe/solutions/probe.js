export async function probe(){ // PEDAGOGY-SOLUTION: D5-NODE-PROBE
 const e=["sync"];process.nextTick(()=>e.push("nextTick"));Promise.resolve().then(()=>e.push("promise"));
 await new Promise(r=>{let n=2,d=()=>{if(--n===0)r()};setTimeout(()=>{e.push("timeout");d()},0);setImmediate(()=>{e.push("immediate");d()});});return e;
}
export async function boundedNextTick(limit){ // PEDAGOGY-SOLUTION: D5-NODE-BOUNDED
 if(limit<0)throw new Error("limit");return await new Promise(r=>{let c=0;function step(){if(c>=limit)return r(c);c++;process.nextTick(step)};process.nextTick(step)});
}
export function yieldImmediate(){ // PEDAGOGY-SOLUTION: D5-NODE-YIELD
 return new Promise(r=>setImmediate(r));
}
