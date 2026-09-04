# chris-binary-toolkit

Safe reverse-engineering and binary-inspection toolkit developed only against owned/benign laboratory targets.

Day 01 begins with an ASCII string extractor and a purpose-built C target. This project will later absorb a hex viewer, PE/ELF structures and controlled process-memory inspection.

No stealth, anti-cheat bypass, credential theft, persistence or third-party compromise is in scope.

## Build and test

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
python benchmarks/benchmark.py
```

## Benchmark methodology

The Day 01 scanner benchmark uses deterministic synthetic buffers at multiple sizes and reports throughput. Before optimizing, profile the current Python loop and form a hypothesis about the bottleneck.

## Limitations

The project currently scans only printable ASCII sequences and operates on files/data owned by the lab. It is not a malware scanner and does not attempt stealth or third-party process manipulation.

## Next milestones

- hex/ASCII view;
- structured PE/ELF header viewer;
- binary diff;
- memory-mapped large-file support;
- controlled process-memory exercises against a self-authored target.
