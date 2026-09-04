# chris-vm

Educational bytecode runtime used to study binary formats, validation and virtual-machine execution.

## Current architecture

`assembly text -> Python assembler -> CLVM file -> C loader -> C++ interpreter`

The file format includes magic/version, entry point, code size and FNV-1a checksum. The VM is stack-based and currently supports arithmetic, printing and relative branches.

## Build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```

On multi-config Visual Studio generators, build/test with `--config Release` and `ctest -C Release`.

## Engineering focus

- bounds checking and malformed-input rejection;
- deterministic bytecode encoding;
- explicit little-endian parsing;
- control-flow validation;
- reproducible integration tests.

## Benchmark question

How much overhead comes from interpreter dispatch versus process startup/I/O? Day 01 establishes a deliberately coarse baseline; later milestones will benchmark the dispatch loop in-process.

## Limitations

This is not a sandbox or production VM. It currently has no linear memory, call frames, verifier-grade control-flow validation or JIT.

## Next milestones

- LOAD/STORE and linear memory;
- virtual registers;
- CALL/RET;
- debugger with breakpoints and stack inspection;
- in-process dispatch benchmark;
- fuzzing of the file parser.
