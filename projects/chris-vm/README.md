# chris-vm

Educational bytecode **platform**: CLVM binary format, assembler, C loader, C++ stack VM, and a JavaScript subset compiler (`js2clvm`) that targets CLVM.

## Como estudar (trilha didática)

Ordem recomendada — teoria antes de “só rodar o CLI”:

1. **Dia 01** [`systems/clvm`](../../days/2026-09-03/systems/clvm) — formato, assembler, VM, JMP/JZ (`TEORIA` + `RESOLUCAO_GUIADA`).
2. **Dia 04** [`clvm_extended`](../../days/2026-09-04/systems/clvm_extended) — CALL/RET, LOAD/STORE, cmp.
3. **Aqui:** [`TEORIA_PASSO_A_PASSO.md`](TEORIA_PASSO_A_PASSO.md) → [`RESOLUCAO_GUIADA_PASSO_A_PASSO.md`](RESOLUCAO_GUIADA_PASSO_A_PASSO.md) → [`docs/STUDY_CHECKLIST_N0.md`](docs/STUDY_CHECKLIST_N0.md) → [`docs/JS_SUBSET.md`](docs/JS_SUBSET.md).
4. **Dia 07 labs:** [`days/2026-09-07`](../../days/2026-09-07) — N1 codegen → N2 verifier → N3 `%` → N4 v2 strings.
5. Mapa: [`docs/LEARNING_PATHS.md`](../../docs/LEARNING_PATHS.md) §3a.

## Pipeline

```text
.js (subset) ──► js2clvm ──► .asm ──► assemble.py ──► .clvm
                                      │
.asm (hand-written) ──────────────────┘
                                         │
                                         ▼
                              C loader (clvm_parse) + rust-validator
                                         │
                                         ▼
                                   C++ interpreter
```

Direct path (skips writing `.asm`): `js2clvm --emit-clvm`.

## ISA (summary)

Extended CLVM v1 (see [FORMAT.md](FORMAT.md)): PUSH…HALT, JMP/JZ, **CALL/RET**, **LOAD/STORE** (256 B linear mem), DROP/SWAP/EQ/LT/JNZ.

## Build

```powershell
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

On multi-config generators use `--config Release` / `ctest -C Release`. Existing tree: `build_ci`.

## JS → bytecode (MVP)

Subset grammar and limits: [docs/JS_SUBSET.md](docs/JS_SUBSET.md).

```powershell
$env:PYTHONPATH = "tools"
python -m js2clvm examples/js/add.js -o out.asm
python tools/assemble.py out.asm out.clvm
./build/Release/clvm.exe out.clvm   # or build/clvm on Unix

# one shot:
python -m js2clvm examples/js/fn_add.js --emit-clvm -o out.clvm
```

## Tools

| Tool | Role |
|------|------|
| `tools/assemble.py` | `.asm` → `.clvm` |
| `tools/js2clvm/` | JS subset → `.asm` / `.clvm` |
| `tools/disasm_clvm.py` | disassemble `.clvm` |
| `tools/verify_clvm.py` | structural + stack-effect checks |
| `tools/inspect_clvm.py` | header dump |

## Engineering focus

- bounds checking and malformed-input rejection;
- deterministic little-endian encoding;
- reproducible integration tests (asm programs + JS goldens).

## Limitations

Not a sandbox or production JS engine. No strings/objects/GC. Local slots use a static memory layout (see JS_SUBSET). No JIT.

## Next milestones

See [MILESTONES.md](MILESTONES.md). Labs: Day 01 `systems/clvm`, Day 04 `clvm_extended`.
