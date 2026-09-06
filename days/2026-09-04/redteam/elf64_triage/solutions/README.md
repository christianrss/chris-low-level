# chris-binary-toolkit

Safe reverse-engineering and binary-inspection toolkit developed only against owned/benign laboratory targets.

Day 01 begins with an ASCII string extractor and a purpose-built C target. Day 02 extends ELF64 triage: Ehdr, program headers, section headers (named via shstrndx), and dynamic symbol listing.

No stealth, anti-cheat bypass, credential theft, persistence or third-party compromise is in scope. No malware samples.

## Build and test

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
python tests/test_elf64.py
python benchmarks/elf64_benchmark.py
python benchmarks/benchmark.py
```

## Benchmark methodology

The ELF64 triage benchmark uses a deterministic synthetic fixture (PHDR + SHDR + dynsym) already in memory and reports `triages_per_s`. Profile before optimizing.

## Limitations

- ELFCLASS64 little-endian only
- Subset of Phdr/Shdr fields; dynsym is name+value triage, not a full dynamic linker
- Not a malware scanner; owned lab samples only

## Next milestones

- hex/ASCII view;
- richer PE/ELF viewers;
- binary diff;
- memory-mapped large-file support;
- controlled process-memory exercises against a self-authored target.

## Day 02 extension

Strict ELF64 identification plus program/section/dynsym triage with synthetic fixtures, truncation checks, and no process access.
