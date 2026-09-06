// TODO [NODE-BACKPRESSURE-01]: implement transform backpressure
import {Transform} from 'node:stream';import {StringDecoder} from 'node:string_decoder';
export class LineTransform extends Transform{constructor(){super({readableObjectMode:true});this.decoder=new StringDecoder('utf8');this.pending='';}_transform(chunk,enc,cb){/* TODO [V2-NODE_TRANSFORM_
B-01] */cb();}_flush(cb){
/* FIXME */cb();}}
