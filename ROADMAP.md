# Roadmap

## Phase 1 - Foundations
- CLVM -> registers, memory, CALL/RET, debugger
- scalar autograd -> tensor storage, strides, broadcasting, GEMM
- MiniObjdump -> ModR/M, symbols, basic blocks, CFG, xrefs
- binary toolkit -> hex view, PE/ELF structures, process memory lab
- renderer -> clipping, textures, camera, rigid-body impulses

## Phase 2 - Integrated systems
- RV32I emulator
- small operating system and drivers in QEMU
- browser parser/layout/painting pipeline
- page-based storage engine and B+tree
- debugger with breakpoints and register/memory views
- CPU tensor runtime with SIMD and threading

## Phase 3 - Research-quality experiments
- interpreter dispatch strategies
- cache-aware GEMM and SIMD ablations
- software rasterizer tiling/SIMD experiments
- quantization accuracy/latency trade-offs
- parser robustness/fuzzing studies
- database page/cache experiments

## Phase 4 - Larger systems
- inference runtime for a small Transformer
- RISC-V system emulator with devices
- browser with scripting runtime
- 3D engine with skeletal animation and GPU backend
- educational hypervisor experiments where platform support permits
