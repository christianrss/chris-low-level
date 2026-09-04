# chris-disassembler

An educational executable inspector and x86-64 disassembler seed. The long-term goal is to understand the mechanisms behind tools such as objdump, PE-bear, IDA and Ghidra by implementing parsing and analysis stages directly.

## Day 01

- detect ELF64 and PE;
- parse section tables;
- locate `.text`;
- decode a small subset of x86-64;
- prepare for basic-block and cross-reference analysis.

## Testing

Integration tests compile a benign target and verify format/section discovery. Malformed input must fail gracefully.

## Next milestones

- separate decoder library from CLI rendering;
- REX prefixes, ModR/M and SIB;
- symbol tables and imports;
- basic blocks and CFG;
- xrefs and function discovery;
- simple IR and data-flow.

## Build, test and benchmark

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
python benchmarks/benchmark.py build/miniobjdump build/test_target
```

On Visual Studio multi-config builds, executables are normally under `build/Release/`.

## Limitations

The decoder intentionally recognizes only a small x86-64 subset. It is not a trustworthy general-purpose disassembler yet; unsupported instructions must remain explicit rather than being guessed.

## References to study as the project grows

Use the official ELF/PE specifications and processor manuals as primary references. External tools such as objdump or dumpbin should be used for validation, not as implementation dependencies.
