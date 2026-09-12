# GFX visual — spec

## Requirement: solutions MUST render

For every module under `days/**/graphics/**` (and Win32 GFX extensions), **solution** executables with `WinMain` / `wWinMain` SHALL:

1. Create a visible top-level window (`CreateWindow` / `CreateWindowEx`).
2. Present frames in a render loop (`StretchDIBits`, OpenGL `SwapBuffers`, or DXGI `Present`).
3. Draw the lab scene (not a placeholder dialog).

`MessageBox` as the only user-visible output is **forbidden** in `solutions/`.

## Exemptions

| Module | Reason |
|--------|--------|
| `os/graphics_reference` | Headless compositor; documented in README |
| `graphics/vulkan_d3d12_resource_states` | State-machine simulation, no Win32 window |
| `resource_state_tracker` | Same class of headless state tracker |

Days 08–11 graphics modules (`shader_stage_fsm`, `gpu_timer_query`, `explicit_barriers`, `pipeline_state_object`, `descriptor_binding_model`, `alpha_blend_scanline`) are **not** exempt — they MUST ship visual `software_win32` + `opengl_win32` solutions.

## Enforcement

`scripts/pedagogy_check_unified.py` → `check_gfx_visual_solutions()` fails on:

- Missing `CreateWindow`
- Missing present heuristic
- MessageBox-only stub (no render loop)

## Starters

Starters MAY keep `MessageBox` + `TODO` stubs; only **solutions** are gated.

## Scaffold

`scripts/scaffold_gfx_trilha.py` (when used) must seed window+DIB or WGL skeleton from `dual_backend_3d`, not MessageBox demos.
