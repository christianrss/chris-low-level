# Architecture
The parser treats the assembly as untrusted bytes. Every read is range-checked. PE parsing is only used to reach the CLI data directory and metadata root; metadata stream/table decoding comes in the next milestone.

`RvaToOffset` is intentionally explicit so the learner sees why an RVA is not a file offset.
