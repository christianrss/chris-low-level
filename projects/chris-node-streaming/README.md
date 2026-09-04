# chris-node-streaming
Node.js/TypeScript production track: streaming newline framing with bounded buffering and an explicit backpressure experiment using only Node core.

Local lab command (Node 22+ with type stripping):
```bash
npm test
npm run demo
npm run bench
```
For production builds, compile TypeScript normally and run an LTS Node release; the source deliberately avoids framework dependencies.
