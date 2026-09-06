# Architecture - chris-binary-toolkit

## Day 02 ELF64 triage layers

```text
bytes
  -> parse_elf64_header        (e_ident + Ehdr fields)
  -> parse_program_headers     (Elf64_Phdr @ phoff, 56 B)
  -> parse_section_headers     (Elf64_Shdr @ shoff, 64 B + shstrndx names)
  -> list_dynamic_symbols      (.dynsym + .dynstr -> name/value)
parallel lens:
  -> extract_ascii_strings
```

All parsers are pure functions over `bytes` with early `ValueError` on truncation/invalid ident. No process attach, no network, no third-party binaries.
