# Architecture — chris-vm

## Components

| Component | Path | Responsibility |
|-----------|------|----------------|
| Format + loader | `include/clvm_format.h`, `src/clvm_loader.c` | Parse 16-byte header, FNV-1a checksum |
| Interpreter | `src/main.cpp` | Stack machine; call stack; 256 B mem |
| Assembler | `tools/assemble.py` | Two-pass labels → bytecode + header |
| JS frontend | `tools/js2clvm/` | Subset JS → AST → CLVM asm (or `.clvm`) |
| Disasm / verify | `tools/disasm_clvm.py`, `tools/verify_clvm.py` | Inspect and validate images |
| Structural Rust check | `rust-validator/` | Opcode walk (optional) |

## Data flow

1. **Source** — hand-written `.asm` or `examples/js/*.js`.
2. **Compile (optional)** — `js2clvm` allocates static local slots, emits labels and CLVM mnemonics.
3. **Assemble** — `assemble.py` resolves labels, writes `CLVM` header + code + checksum.
4. **Load** — `clvm_parse` rejects bad magic/size/checksum/entry.
5. **Execute** — PC + data stack + call stack + linear memory; `PRINT` to stdout; `HALT` exits 0.

## Design decisions

- **One ISA file format** for labs and the capstone; Day 04 opcodes are first-class here.
- **JS compiles to asm text first** so students can read the lowering; `--emit-clvm` reuses the same assembler core.
- **Static slot bases per function** avoid a frame-pointer opcode in v1 (no recursive re-entry of the same function).
- **chris-js stays separate** — its bytecode is not CLVM; no shared VM.

## Related docs

- [FORMAT.md](../FORMAT.md) — wire format
- [JS_SUBSET.md](JS_SUBSET.md) — language surface and limits
- [MILESTONES.md](../MILESTONES.md) — roadmap
