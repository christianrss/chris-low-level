# Day 01 - Consolidated Low-Level Engineering Lab

This day now contains the original core exercises plus the first executable milestones from the expanded portfolio directive.

## Original cores
- Systems: CLVM binary format + VM.
- AI: manual linear regression + scalar autograd.
- Safe RE: benign binary analysis.
- Tooling: MiniObjdump.
- Graphics: shared 3D/physics core and dual Win32 backend study.

## Added foundations
- Assembly x86-64 ABI.
- Tiny CPU fetch/decode/execute.
- Legacy BIOS boot sector.
- Terminal ESC/CSI parser.
- Incremental HTTP parser.
- P2P gossip simulator.
- Local toy blockchain.
- Driver descriptor-ring simulator.

Open `Treino_LowLevel_Unificado_2026-09-03.docx` for the master guided document. Each module also contains Markdown theory/resolution/testing/benchmark notes and `starter/` + `solutions/`.


## Pedagogical audit
All 13 Day 01 modules were re-audited after a starter/resolution mismatch was found in `graphics/dual_backend_3d`. The corrected modules use tagged TODO IDs that are mechanically cross-checked against the guided resolution, test guide and solution. Run `python scripts/pedagogy_check.py` from the repository root. See `VALIDATION_DAY01.md`.
