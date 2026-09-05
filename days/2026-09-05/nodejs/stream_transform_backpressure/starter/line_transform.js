import { Transform } from 'node:stream';
import { StringDecoder } from 'node:string_decoder';

export class LineTransform extends Transform {
    constructor() {
        super({ readableObjectMode: true });
        this.decoder = new StringDecoder('utf8');
        this.pending = '';
    }

    _transform(chunk, encoding, callback) {
        // TODO [NODE-XFORM-01]: dividir linhas UTF-8 com suporte a multibyte
        callback();
    }

    _flush(callback) {
        // TODO [NODE-XFORM-01]: emitir linha pendente no final
        callback();
    }
}
