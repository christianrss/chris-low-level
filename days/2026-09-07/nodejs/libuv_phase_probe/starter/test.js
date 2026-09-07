import {probe,boundedNextTick,yieldImmediate} from "./probe.js";
const e=await probe();
// PEDAGOGY-TEST: D5-NODE-PROBE
if(e[0]!=="sync"||!e.includes("nextTick")||!e.includes("promise")||!e.includes("timeout")||!e.includes("immediate"))throw Error("probe");
const macro=Math.min(e.indexOf("timeout"),e.indexOf("immediate")); if(e.indexOf("promise")>macro||e.indexOf("nextTick")>macro)throw Error("ordering");
// PEDAGOGY-TEST: D5-NODE-BOUNDED
if(await boundedNextTick(25)!==25)throw Error("bounded");
// PEDAGOGY-TEST: D5-NODE-YIELD
let x=false;setImmediate(()=>x=true);await yieldImmediate();if(!x)throw Error("yield");
console.log("chris-node-phase tests passed");