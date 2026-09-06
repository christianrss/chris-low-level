# Complete Track Map

## Core systems
C, C++, Rust, Python, x86-64/ARM64/RISC-V Assembly, ABI, memory, ELF/PE/COFF, loaders/linkers, compilers, VM/JIT, OS, drivers, storage, networking, concurrency, SIMD and profiling.

**Rust labs (Dia 2026-09-06):** `rust/rle_byte_codec` (CHRLE com `Result`/slices) e `rust/gzip_member_parse` (parser estrutural RFC 1952). Intro opcional no Dia 01: `systems/clvm/.../rust-validator`.

## Architecture and hardware
Digital logic, datapath, pipelines, branch prediction, OoO concepts, cache/TLB/coherence, MMIO/DMA, PCIe, USB, I2C/SPI/UART/GPIO, ACPI, SMBIOS, virtio and device protocols.

## Boot and firmware
Reset, BIOS legacy boot, UEFI, boot protocols, coreboot/LinuxBoot concepts, SPI flash, ACPI tables, firmware security and recovery.

## Toolchains
Assembler, linker, loader, object writer, disassembler, debugger, symbolizer, stack unwinder and binary-inspection tooling.

## Kernel and filesystems
Interrupts/syscalls, scheduler, SMP, memory management, VFS, block layer, page cache, FAT/ext-style filesystems, FUSE, networking and drivers.

## Terminal/network/crypto
Terminal emulator, shell, PTY, SSH, key generation/formats, HTTP/FTP/DNS/WebSocket/MQTT/RPC and cryptographic composition.

## P2P/distributed/blockchain
Gossip, DHT, swarming, CAS, Raft, Merkle trees, mempool, toy consensus and local test chains.

## AI systems
Autograd, tensor runtime, CPU/GPU kernels, quantization, inference, training, RL and serving.

## Safe reverse engineering
Owned/benign binaries and labs only: assembly, calling conventions, PE/ELF, debugging, deobfuscation, instrumentation, YARA/telemetry and defensive analysis.

## Graphics/media
Software rendering, real-time 3D, physics, animation, GPU APIs, image editor internals, audio/video pipelines and profiling.

## "Magic" backlog
Allocator, GC, regex engine/JIT, async runtime, green threads, lock-free queues, profiler/tracer, eBPF-like VM, userspace TCP/IP stack, Git-like CAS, container runtime, package manager, COW filesystem, search engine, window manager/compositor, remote desktop, codec, WASM runtime, emulator/VM, hypervisor, database/query engine and browser engine.


## Managed runtimes and production stacks
- .NET/C# production senior track + CLR internals from scratch.
- Node.js/TypeScript production senior track + JavaScript/VM/V8/libuv internals from scratch.
- See `docs/RUNTIME_STACKS_DOTNET_NODE.md`.
