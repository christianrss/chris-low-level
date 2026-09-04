# chris-renderer

A low-level 3D/physics/animation project that compares mechanisms implemented manually with a real graphics API backend.

## Day 01 architecture

The portable `scene_core` owns math, hierarchical animation and physics. On Windows the same scene is presented by:

- a CPU software rasterizer using Win32 only for window/framebuffer presentation;
- an OpenGL backend using WGL.

This separation makes the abstraction boundary visible.

## Tests

Portable tests validate matrix transforms, physics and scene invariants. They intentionally avoid GPU dependencies.

## Benchmark direction

Day 01 measures the shared CPU core. Later experiments will compare software rasterization strategies, resolution scaling, tiling/SIMD and GPU timing.

## Build and test

Portable core on Linux/macOS:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
./build/core_benchmark
```

Windows/MSVC:

```bat
cmake -S . -B build -A x64
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

The Win32 software/OpenGL backends are built only on Windows. `NOMINMAX` is defined to prevent legacy `windows.h` macros from breaking `std::min/std::max`.

## Limitations

Day 01 physics uses a simplified floor collision and restitution model. Animation is transform hierarchy rather than skeletal skinning. The OpenGL backend is educational and not yet a production renderer.

## Next milestones

- camera controls and clipping;
- texturing and perspective-correct interpolation;
- quaternion animation;
- collision shapes and impulses;
- controlled CPU software-rasterizer benchmark;
- GPU timing and RenderDoc-based inspection.
