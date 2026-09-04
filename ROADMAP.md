# Long-Term Roadmap

This roadmap aims at expert-level systems depth. Covering the topics is not the same as matching the lifetime experience of engineers such as Simon Tatham, Ron Minnich, Fabrice Bellard, Michael Abrash or H. Peter Anvin. The path therefore includes not only implementation, but specification reading, debugging, measurement and eventual upstream work.

## Phase 0 - Engineering habits (continuous)

- build from a clean checkout;
- tests before/with features;
- regression tests for every discovered bug;
- sanitizers, fuzzing and static analysis where appropriate;
- reproducible benchmark methodology;
- ADRs for meaningful design choices;
- read specifications instead of relying only on tutorials;
- learn `git bisect`, code review and patch archaeology.

## Phase 1 - Machine foundations

- digital logic: gates -> latches -> registers -> ALU -> datapath;
- tiny CPU simulator with fetch/decode/execute;
- x86-64/ARM64/RISC-V instruction formats and ABI;
- Assembly functions, syscalls, stack frames and atomics;
- cache/TLB/virtual-memory experiments;
- binary formats: ELF, PE/COFF, object files and relocations.

Milestones: `chris-cpu`, `chris-memory-sim`, `chris-assembly-lab`.

## Phase 2 - Toolchain from source to executable

- `chris-nasm`: lexer, parser, expressions, symbols, labels, sections, directives;
- x86-64 prefixes, opcode maps, ModR/M, SIB, displacements and immediates;
- relocations and ELF/COFF object generation;
- static linker: sections, symbol resolution, relocations, archives;
- dynamic-linking concepts: GOT/PLT, PIC/PIE, TLS;
- DWARF/unwind/symbolization and CodeView/PDB concepts.

Milestones: `chris-nasm`, `chris-linker`, `chris-loader`, `chris-disassembler`.

## Phase 3 - Boot, BIOS, UEFI and firmware

- reset vector and x86 reset state;
- real mode, A20, GDT, protected mode, page tables and long mode;
- MBR/VBR, GPT, El Torito, PXE and chainloading;
- Linux boot protocol and Multiboot;
- UEFI applications/drivers, Boot Services and Runtime Services;
- PE/COFF in UEFI, memory map and `ExitBootServices`;
- PEI/DXE/BDS concepts, firmware volumes and capsules;
- coreboot/LinuxBoot/u-root concepts;
- PCI enumeration, ACPI/SMBIOS, APIC/IOAPIC, EC/Super I/O, SPI flash;
- vendor silicon-init interfaces conceptually (FSP/AGESA);
- Secure Boot, measured boot, TPM/PCRs, rollback protection and recovery.

Milestones: `chris-boot`, `chris-uefi`, `chris-firmware-lab`.

## Phase 4 - Kernel and drivers

- early kernel entry, GDT/IDT, exceptions, interrupts and syscalls;
- page allocator, virtual memory and slab-like allocator;
- scheduler, context switch, SMP/per-CPU data, atomics/spinlocks;
- VFS, filesystems, block layer, page cache and mmap;
- network stack integration;
- PCI/MMIO, IRQ/MSI/MSI-X, DMA, descriptor rings and queues;
- PS/2 and USB HID keyboard/mouse;
- virtio/e1000 network driver;
- UVC/webcam pipeline;
- framebuffer/virtio-gpu educational driver;
- SATA/NVMe queue models;
- power-management and crash-debugging concepts.

Milestones: `chris-kernel`, `chris-vfs`, `chris-pci`, `chris-net-driver`, `chris-hid-driver`, `chris-uvc`, `chris-gpu-driver`.

## Phase 5 - Emulation, virtualization and JIT

- interpreter and deterministic CPU tests;
- MMU, timers, interrupts and device models;
- UART, block, network and virtio devices;
- snapshots and deterministic replay concepts;
- IR design, dynamic binary translation and JIT;
- KVM/hardware-virtualization concepts and hypervisor labs where safe.

Milestone: `chris-machine`.

## Phase 6 - Compiler/runtime

- C-like lexer/parser/type system;
- symbols, scopes and diagnostics;
- x86-64/RISC-V code generation;
- embedded assembler and linker;
- ELF/PE output;
- JIT/library-style compiler;
- allocator, GC experiments, async runtime and coroutine scheduler.

Milestones: `chris-tcc`, `chris-runtime`.

## Phase 7 - Terminal, protocols and cryptographic systems

- ECMA-48 terminal parser, UTF-8, scrollback, PTY/ConPTY;
- shell: parser, pipes, redirection, signals and job control;
- terminal multiplexer and session model;
- TCP client/server fundamentals;
- HTTP, FTP, DNS, WebSocket, SMTP/POP3/IMAP educational implementations;
- SSH transport/auth/channels/PTY educational stack;
- key formats, fingerprints, Base64 and key-generation utility using audited crypto;
- HMAC, AEAD, KDF, CSPRNG and constant-time concepts.

Milestones: `chris-terminal`, `chris-shell`, `chris-http`, `chris-ssh`.

## Phase 8 - P2P, distributed systems and blockchain

- peer discovery, gossip, DHT/Kademlia and swarming;
- content-addressed storage and chunk replication;
- BitTorrent-like transfer model;
- distributed logs and Raft;
- hash chains, Merkle trees, UTXO/account models, mempool;
- toy PoW and consensus/fork simulations;
- local-only toy cryptocurrency, wallet/explorer/RPC;
- failure injection, partition tests and performance studies.

Milestones: `chris-p2p`, `chris-raft`, `chris-chain`.

## Phase 9 - Graphics/performance/multimedia

- software rasterizer -> clipping -> texturing -> tiling;
- fixed-point and SIMD experiments;
- cache-aware data structures;
- OpenGL/Vulkan/Direct3D comparisons;
- GPU scheduling/memory concepts and educational driver work;
- audio PCM/resampling/mixing/FFT;
- container/codecs and video playback pipeline;
- frame pacing and latency measurement.

Milestones: `chris-renderer`, `chris-media-engine`.

## Phase 10 - ML systems/research engineering

- scalar autograd -> tensors -> strides/broadcasting;
- GEMM, convolution and attention kernels;
- SIMD/threading/cache tiling;
- Transformer inference runtime;
- quantization and accuracy/latency studies;
- GPU/CUDA kernels;
- training loops/optimizers;
- serving, batching, KV cache and distributed inference concepts;
- reproducible research experiments and ablations.

Milestones: `chris-autograd`, `chris-tensor`, `chris-inference`.

## Phase 11 - Real-world engineering

- read and modify mature codebases;
- reproduce bugs from issue trackers;
- submit small upstream patches;
- participate in code review;
- maintain releases and compatibility;
- write technical reports/posts with measured claims;
- eventually target contributions to Linux, coreboot, QEMU, NASM, LLVM/Clang, FFmpeg or comparable projects.
