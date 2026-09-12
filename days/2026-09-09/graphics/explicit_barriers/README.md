# explicit_barriers

Modulo **visual** C++: `software_win32` + `opengl_win32` + `core/` testavel.

## TODOs

- `GFX-BAR-VALID`
- `GFX-BAR-APPLY`
- `GFX-BAR-TICK`

## Build

```powershell
cmake -S starter -B starter/build_ci -G Ninja
cmake --build starter/build_ci
ctest --test-dir starter/build_ci --output-on-failure
# demos: starter/build_ci/explicit_barriers_sw.exe  /  explicit_barriers_gl.exe
```
