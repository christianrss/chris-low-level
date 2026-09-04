# Architecture

`TinyCpu` owns 64 KiB or less of byte-addressed memory, four 16-bit registers, a 16-bit program counter and a halt flag.

The instruction loop is intentionally explicit: `fetch opcode -> fetch operands -> validate -> execute -> update architectural state`. Multi-byte immediates are little-endian so endianness is visible in the code.
