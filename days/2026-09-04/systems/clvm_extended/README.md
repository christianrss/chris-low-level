# Ordem de estudo

1. `TEORIA_PASSO_A_PASSO.md` + paper-trace de `add2.asm` e `max_loop.asm`
2. `TODO [CLVM-EXT-01]` em `starter/tools/assemble.py`
3. `TODO [CLVM-EXT-02]` / `03` / `04` em `starter/src/main.cpp`
4. cmake/ctest — `add2`→8, `mem_demo`→42, `max_loop`→0..3+1
5. Compare `solutions/`

---

# CLVM extended ISA — Dia 2026-09-04

Evolução completa da VM do Dia 01 num único lab: **CALL/RET**, **LOAD/STORE**, comparações e stack ops.

## Pré-requisitos

- Dia 01 `systems/clvm` completo (ou gabarito entendido)
- CMake 3.20+, C11/C++17, Python 3.10+

## Build starter (esperado FAIL)

```powershell
cd days/2026-09-04/systems/clvm_extended/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

## Build solutions (esperado PASS)

```powershell
cd days/2026-09-04/systems/clvm_extended/solutions
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

## Portar

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-vm` |
| Depois | `js2clvm` (JS → CLVM) — ver TEORIA/RESOLUCAO no capstone |
| Commit | `feat(vm): extended ISA from day04 clvm_extended` |
