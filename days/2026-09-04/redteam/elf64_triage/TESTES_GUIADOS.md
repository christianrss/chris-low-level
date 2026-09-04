# Testes guiados — ELF64 triage

```bash
python projects/chris-binary-toolkit/tests/test_elf64.py
```

Os testes usam um header ELF64 sintético construído em memória. Eles validam machine/entry/counts e exigem falha para truncation e magic incorreto.

Para o alvo benigno do próprio laboratório:
```bash
cmake -S projects/chris-binary-toolkit -B build/chris-binary-toolkit -DCMAKE_BUILD_TYPE=Release
cmake --build build/chris-binary-toolkit --config Release
ctest --test-dir build/chris-binary-toolkit --output-on-failure
```
