# Directive coverage matrix

This document prevents the curriculum from drifting away from the long-term goal. It distinguishes **implemented Day 01 milestones** from **explicit roadmap work**. A topic appearing here does not mean it is already complete.

| Area | Day 01 evidence | Long-term direction |
|---|---|---|
| C/C++/Python/Rust/Assembly | CLVM mixed-language lab, x86-64 Assembly ABI lab | multi-architecture systems code, Rust components, optimized kernels |
| x86-64 / ARM64 / RISC-V | x86-64 encoding + ABI foundations | ISA comparison, privilege modes, paging, atomics, SIMD/vector, boot |
| CPU architecture | `chris-cpu` fetch/decode/execute simulator | pipeline, hazards, cache/TLB, OoO concepts, SoC simulation |
| Memory/performance | benchmark methodology + renderer/VM experiments | cache hierarchy, NUMA, allocators, SIMD, memory ordering, profiling |
| Binary formats | CLVM format + ELF/PE inspection | ELF/PE/COFF writers, relocations, debug formats, firmware formats |
| Assembler/toolchain | `chris-nasm` real byte encodings for a tiny subset | expressions, labels, macros, ModR/M/SIB, relocations, object files, linker |
| Bootloaders | legacy BIOS 512-byte boot-sector model + NASM source | reset vector, real/protected/long mode, Linux protocol, Multiboot, PXE |
| BIOS/UEFI/firmware | boot foundations and architecture notes | UEFI apps/drivers, PEI/DXE/BDS, coreboot-like labs, SPI/ACPI/SMBIOS |
| Firmware security | scope/read-map established | Secure Boot, measured boot, TPM/PCRs, signing, rollback/recovery |
| Kernel | prerequisite CPU/boot/descriptor work | interrupts, syscalls, VM, scheduler, SMP, VFS, network, modules |
| Filesystems/storage | roadmap + binary/storage foundations | FAT/ext-style image FS, VFS, FUSE, block layer, NVMe queue model |
| Drivers/hardware | `chris-driver-lab` descriptor ring simulator | PCI, MMIO, IRQ/MSI-X, DMA, virtio/e1000, HID, UVC, GPU, NVMe |
| Terminal/shell | `chris-terminal` incremental ANSI/ECMA-48 parser | rendering, UTF-8, PTY/ConPTY, shell, job control, multiplexer |
| SSH/key tooling/crypto | architecture/safety scope | transport/KEX/auth/channels, key formats, audited crypto, key generator |
| HTTP/FTP/DNS/etc. | `chris-http` incremental request parser | sockets, HTTP server/client, FTP, DNS, WebSocket, MQTT, RPC |
| P2P | `chris-p2p` deterministic gossip | discovery, DHT/Kademlia, swarming, CAS, failure/partition experiments |
| Blockchain/cryptocurrency | `chris-chain` hash/Merkle/toy-PoW lab | mempool, UTXO, wallet, RPC, explorer, forks/reorgs, local testnet only |
| Safe reverse engineering | benign reversing + disassembler/binary toolkit | debugger, CFG/xrefs, deobfuscation, instrumentation, defensive telemetry |
| Adversarial systems | safety boundary and future lab design | benign fleet/C2 simulation, beacon analysis, detection, hardening |
| Obfuscation/deobfuscation | scoped to owned toy binaries | CFG simplification, string recovery, toy opaque predicates/packing |
| Injection/hooking | defensive/observability scope | own-process instrumentation, profiler hooks, trampolines, IAT concepts |
| Emulation/virtualization | VM + CPU simulator foundations | MMU/devices, virtio, snapshots, DBT/JIT, hypervisor concepts |
| Compiler/runtime | VM/autograd/toolchain prerequisites | tiny C compiler, codegen, embedded assembler/linker, JIT, allocator/GC |
| Graphics | shared 3D/physics core + software/OpenGL tracks | rasterizer, clipping, texturing, SIMD, GPU APIs, driver concepts |
| Multimedia | roadmap | image editor internals, audio engine, codecs, video timeline/compositor |
| AI/ML systems | manual gradient training + scalar autograd | tensor runtime, GEMM, attention, quantization, CUDA, inference/serving |
| Testing | tests in every implemented project/module | property/fuzz/golden/regression/system tests and bug-driven regressions |
| Benchmarks | consolidated reproducible Day 01 baselines | controlled experiments, profiling, ablations and performance archaeology |
| Research profile | research notes + hypothesis methodology | experiment logs, papers/spec reading, technical reports, reproducibility |
| Portfolio/Git | repo-ready layout, CI, commit plan, progress/roadmap | releases, external users, issue history, upstream contributions |
| Expert engineering | reading maps + long-lived projects | Linux/coreboot/QEMU/NASM/LLVM/FFmpeg-style upstream work when ready |

## Long-lived milestone projects

The curriculum deliberately converges on a smaller set of deep systems instead of creating hundreds of shallow repositories:

- `chris-nasm` + future `chris-linker`/`chris-loader`;
- `chris-boot` + future `chris-uefi`/`chris-firmware-lab`;
- future `chris-kernel`, VFS and hardware drivers;
- future `chris-machine` emulator/DBT/JIT;
- future `chris-tcc` compiler/runtime;
- `chris-terminal` + future shell/SSH stack;
- `chris-p2p`/`chris-chain` + distributed-systems experiments;
- `chris-renderer` and GPU/performance work;
- `chris-autograd` -> tensor runtime -> inference/training systems.

The intended progression is: **guided implementation -> independent extension -> specification compliance -> fuzzing/benchmarking -> real bug reports -> upstream contribution/original work**.
