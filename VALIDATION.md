# Validation report - 2026-09-03 consolidated repository

This file records what was actually validated before packaging. It deliberately distinguishes portable tests from platform/hardware milestones that were not available in the validation environment.

## Repository quality

- `python scripts/quality_check.py`: PASS after consolidation.
- Source formatting/minification guard: PASS for the files checked by the repository script.
- Build outputs, caches and generated binaries are removed before packaging.

## Portable project tests

All 14 cumulative Day 01 projects passed their available portable tests in the validation environment:

1. `chris-vm`
2. `chris-autograd`
3. `chris-disassembler`
4. `chris-binary-toolkit`
5. `chris-renderer` portable core
6. `chris-assembly-lab` on Linux x86-64 System V
7. `chris-cpu`
8. `chris-nasm`
9. `chris-boot` structural byte-model tests
10. `chris-terminal`
11. `chris-http`
12. `chris-p2p`
13. `chris-chain`
14. `chris-driver-lab`

The aggregate helper configures projects independently. In this container a single clean aggregate invocation exceeded the execution harness time limit after `chris-http`; the remaining projects were then configured/built/tested individually and passed. This is a harness-timeout note, not a test failure.

## Benchmarks

`python scripts/run_all_benchmarks.py`: PASS in the validation environment. Consolidated results and limitations are stored in:

- `benchmarks/results-2026-09-03.md`
- `benchmarks/results-2026-09-03.json`

The results are baselines for methodology and regression work, not universal performance claims.

## Master training document

- File: `days/2026-09-03/Treino_LowLevel_Unificado_2026-09-03.docx`
- Rendered page count: 78 pages.
- The consolidated document was rendered to page images before packaging and visually reviewed for clipping/overlap/layout issues. The original 58-page section retained its previously validated layout; the changed cover and appended consolidated section were rechecked after the final edit.

## Important environment limitations

- Win32/WGL/OpenGL frontends were not executed here because this host has no Windows SDK/MSVC. The repository CI contains a Windows job, but that CI job has not been claimed as executed by this local validation.
- NASM and QEMU were not required for the Day 01 `chris-boot` structural tests, so the actual boot sector was not assembled and booted in QEMU in this environment. That becomes a later reproducible lab milestone.
- `chris-driver-lab` is a userspace descriptor-ring simulator. It is not yet a kernel driver and does not perform DMA/MMIO.
- Firmware, BIOS/UEFI, PCI, UVC, virtio, NVMe and GPU-driver work beyond the Day 01 simulations are roadmap milestones, not falsely represented as completed implementations.
- `chris-assembly-lab` currently executes only on Linux x86-64 System V; future milestones add Windows x64, ARM64 and RISC-V variants.
- Cryptography, SSH, lateral-movement simulation, obfuscation and adversarial-system topics follow the safety boundaries in `docs/SAFETY_BOUNDARIES.md`; production cryptography must use audited primitives/libraries.
