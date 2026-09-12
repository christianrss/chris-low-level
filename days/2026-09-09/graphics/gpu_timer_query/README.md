# gpu_timer_query

Modulo **visual** C++: `software_win32` + `opengl_win32` + `core/` testavel.

## TODOs

- `GFX-TQ-BEGIN`
- `GFX-TQ-END`
- `GFX-TQ-READ`

## Build

```powershell
cmake -S starter -B starter/build_ci -G Ninja
cmake --build starter/build_ci
ctest --test-dir starter/build_ci --output-on-failure
# demos: starter/build_ci/gpu_timer_query_sw.exe  /  gpu_timer_query_gl.exe
```
