import { Readable, Writable, pipeline } from 'node:stream';
import { LineFramer } from './line-framer.ts';

const source = Readable.from(['alpha\nbe', 'ta\ngamma\n']);
let writes = 0;
const sink = new Writable({
  objectMode: true,
  highWaterMark: 1,
  write(line: string, _encoding, callback) {
    writes++;
    setTimeout(() => { console.log(`sink:${line}`); callback(); }, 5);
  }
});
pipeline(source, new LineFramer(), sink, (error) => {
  if (error) { console.error(error); process.exitCode = 1; }
  else console.log(`completed writes=${writes}`);
});
