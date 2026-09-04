# Day 01 — pedagogical consistency audit

Audit performed after a learner reported that guided instructions did not match the starter code, especially `graphics/dual_backend_3d`.

## Acceptance rule
For every Day 01 programming module, the audited version requires:
- a real starter that configures/builds;
- tagged code TODOs (`TODO [ID]`) at the exact places the learner edits;
- every TODO ID referenced by the guided resolution and test guide;
- a corresponding non-TODO implementation in `solutions/`, marked `PEDAGOGY-SOLUTION: ID`;
- tests registered by CMake when a CMake test directory exists;
- guided research (`PESQUISA_GUIADA.md`);
- operational instructions: exact path/function, code to enter, build/run/test, expected failure/success and debugging.

## Structural gate
`python scripts/pedagogy_check.py`

Result: **PASS — 13 modules, 45 starter TODO mappings**.

`python scripts/quality_check.py`

Result: **PASS — 698 files checked** in the local audit workspace.

## Starter vs solution execution
Portable modules were configured/built from both `starter/` and `solutions/`. The expected invariant was observed: the starter builds and its tests fail because the exercise TODO is incomplete; the solution builds and passes.

Verified in this audit:
- `ai/linear_autograd`: starter fails intended convergence/autograd test; solution passes 2/2.
- `architecture/toy_cpu`: starter fails intended CPU-step test; solution passes.
- `assembly/x86_64_abi_sum`: starter fails intended ABI sum test; solution passes on Linux x86-64 System V.
- `blockchain/toy_chain`: starter fails intended Merkle/chain behavior; solution passes.
- `boot/legacy_bootsector`: starter fails intended boot-image signature/layout test; solution passes structural test.
- `graphics/dual_backend_3d`: portable core starter fails the intended guided TODO tests; solution passes. Win32/WGL frontends are not claimed as executed on this Linux host.
- `hardware/descriptor_ring`: starter fails intended ring behavior tests; solution passes.
- `network/http_parser`: starter fails intended fragmented-request test; solution passes.
- `p2p/gossip`: starter fails intended propagation test; solution passes.
- `redteam/benign_reversing`: starter fails intended ASCII/YARA semantic tests; solution passes 2/2.
- `systems/clvm`: starter fails on intended unimplemented opcode/assembler path; solution integration test passes.
- `terminal/ansi_parser`: starter fails intended CSI/state test; solution passes.
- `tooling/miniobjdump`: starter fails intended PE/ELF parsing expectations; solution passes integration test.

## dual_backend_3d repair
The previous guide referred to missing or mismatched concepts such as `look_at`, `frame_dt`, generic “equivalent” functions and camera state without a concrete insertion path. The audited starter/solution now expose explicit TODOs for camera helpers/state/update, culling, Lambert lighting and software rasterization; the resolution references those exact TODO IDs and concrete files/functions.

## CI regression protection
GitHub Actions now runs `scripts/pedagogy_check.py` in addition to the normal quality/tests gate, so a future mismatch between starter, resolution, test guide and solution fails CI instead of reaching the learner.
