// PEDAGOGY-SOLUTION: ND-GZ-01
// PEDAGOGY-SOLUTION: ND-GZ-03
import { Transform } from 'node:stream';
import zlib from 'node:zlib';

export class GunzipTransform extends Transform {
    constructor() {
        super();
        this.gunzip = zlib.createGunzip();
        this.bytesIn = 0;
        this.bytesOut = 0;
        this.backpressurePauses = 0;
        this.gunzip.on('data', (chunk) => {
            this.bytesOut += chunk.length;
            const ok = this.push(chunk);
            if (!ok) {
                this.gunzip.pause();
                this.backpressurePauses++;
            }
        });
        this.gunzip.on('end', () => this.push(null));
        this.gunzip.on('error', (err) => this.destroy(err));
        this.on('drain', () => this.gunzip.resume());
    }

    _transform(chunk, encoding, callback) {
        this.bytesIn += chunk.length;
        const ok = this.gunzip.write(chunk);
        if (!ok) {
            this.gunzip.once('drain', callback);
            return;
        }
        callback();
    }

    _flush(callback) {
        this.gunzip.end(callback);
    }
}
