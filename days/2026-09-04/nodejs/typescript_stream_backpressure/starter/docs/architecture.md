# Architecture
`LineFramer` is a `Transform` whose writable side accepts bytes and readable side emits logical lines. It buffers only an incomplete trailing line and enforces `maxLineBytes` to bound memory growth. The demo places a slow `Writable` with `highWaterMark=1` downstream so Node's stream machinery can exert backpressure instead of the producer manually polling sink speed.
