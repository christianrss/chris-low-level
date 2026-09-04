# Architecture

The parser buffers fragmented input until the header terminator is present, parses the request line and headers, then waits for the declared body length. The later socket layer will be separate so protocol parsing can be fuzzed and tested without networking.
