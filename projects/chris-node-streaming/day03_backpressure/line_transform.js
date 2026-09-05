// SOLVES [NODE-XFORM-01]
// SOLVES [NODE-BACKPRESSURE-02]
import { Transform } from 'node:stream'; import { StringDecoder } from 'node:string_decoder';
export class LineTransform extends Transform{ constructor(){super({readableObjectMode:true});this.decoder=new StringDecoder('utf8');this.pending='';} _transform(chunk,enc,cb){ const text=this.pending+this.decoder.write(chunk); const parts=text.split('\n'); this.pending=parts.pop()??''; for(const line of parts)this.push(line); cb(); } _flush(cb){ const rest=this.pending+this.decoder.end(); if(rest.length)this.push(rest); cb(); }}
