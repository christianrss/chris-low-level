# Architecture

Input bytes enter an incremental state machine (`Ground`, `Escape`, `Csi`). Printable bytes update a fixed text grid. CSI final bytes mutate cursor or display state. The parser retains state across `feed()` calls so fragmented reads behave like real sockets/PTY streams.
