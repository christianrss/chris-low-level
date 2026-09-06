# chris-compress

Capstone cumulativo do Day 06 — CLI mínima que encadeia RLE e zlib stored deflate portados dos labs.

## Build

```powershell
cmake -S projects/chris-compress -B build/chris-compress -A x64
cmake --build build/chris-compress --config Release
ctest --test-dir build/chris-compress -C Release
```

## Uso

```powershell
.\build\chris-compress\Release\chris_compress.exe rle hello
.\build\chris-compress\Release\chris_compress.exe zlib hello
```

## Origem

- `days/2026-09-06/systems/rle_byte_codec`
- `days/2026-09-06/tooling/zlib_gzip_containers`
