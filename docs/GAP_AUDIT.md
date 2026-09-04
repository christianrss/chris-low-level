# Gap Audit — 2026-09-04

This audit compares the current roadmap against the goal of becoming a deep cross-stack systems/research engineer. The repository already covers machine architecture, boot/firmware, kernels/drivers, toolchains, emulation, networking/protocols, P2P/blockchain, graphics, ML systems, reverse engineering, algorithms and quantum-computing plans. The following gaps are now first-class tracks rather than incidental topics.

## P0 — highest-value gaps

### Formal methods and verification
Build beyond tests: invariants, safety/liveness, temporal logic, model checking, SAT/SMT, symbolic execution, refinement and small machine-checked proofs. Target projects: `chris-model-checker`, `chris-sat`, `chris-smt-lite`, `chris-symbolic`, `chris-verifier`.

### HDL, FPGA, ASIC and EDA
Move below software architecture into RTL: Verilog/SystemVerilog, testbenches, CDC, timing, synthesis, STA, FPGA, RISC-V softcores, cache controllers, NoCs, systolic accelerators and an educational RTL-to-GDSII flow. Target projects: `chris-riscv-rtl`, `chris-fpga-soc`, `chris-cache-rtl`, `chris-noc`, `chris-accelerator-rtl`, `chris-eda-lab`.

### GPU/accelerator compiler and runtime stack
Study CUDA/HIP/PTX/SPIR-V concepts, warp execution, memory hierarchy, tiling/fusion/autotuning, then SSA/LLVM IR/MLIR-style lowering. Connect generated kernels to accelerator architecture. Target projects: `chris-kernel-lang`, `chris-mlir-lite`, `chris-gpu-runtime`, `chris-autotuner`, `chris-accelerator-sim`.

### Distributed ML and collective communication
Add Ring/Tree AllReduce, AllGather, ReduceScatter, AllToAll, topology awareness, RDMA/RoCE/InfiniBand concepts, tensor/data/pipeline/expert parallelism, overlap, checkpointing and failure recovery. Target projects: `chris-collectives`, `chris-distributed-train`, `chris-topology-sim`, `chris-checkpoint`.

### HPC and numerical computing
Add IEEE-754 behavior, numerical stability/conditioning, BLAS-like kernels, dense/sparse linear algebra, FFT, iterative solvers, OpenMP/MPI concepts and strong/weak scaling. Target projects: `chris-numerics`, `chris-blas`, `chris-sparse`, `chris-fft`, `chris-mpi`, `chris-hpc-bench`.

## P1 — major systems gaps

### Embedded and real-time systems
Bare-metal MCU startup, linker scripts, vector tables, ISRs, DMA, timers, ADC/PWM, buses, watchdogs, power, deadlines, priority inversion and RTOS primitives. Target projects: `chris-mcu`, `chris-rtos`, `chris-hal`, `chris-sensor-hub`.

### Databases and storage engines
Pages, buffer pools, WAL/recovery, B+ trees, LSM/SSTables/compaction, MVCC, isolation/serializability, query planning/optimization, joins, vectorized execution and column stores. Target projects: `chris-db`, `chris-btree`, `chris-lsm`, `chris-wal`, `chris-query`, `chris-columnstore`.

### High-performance networking
IPv6/routing/LPM/load balancing, QUIC concepts, congestion control, eBPF/XDP, DPDK-style userspace packet processing, zero-copy/batching/RSS/offloads, io_uring concepts, RDMA and time synchronization. Target projects: `chris-router`, `chris-loadbalancer`, `chris-quic`, `chris-ebpf`, `chris-xdp`, `chris-packet-engine`, `chris-rdma-sim`.

### Observability, reliability and fault tolerance
Metrics/logs/traces, flamegraphs, crash analysis, retries/backpressure/circuit breakers, checkpoint/restart, fault injection, chaos experiments, tail latency and capacity reasoning. Target projects: `chris-tracer`, `chris-profiler`, `chris-observability`, `chris-chaos-lab`, `chris-fault-injector`.

### Distributed systems depth
Logical clocks, causality, failure detectors, leases, consensus, CRDTs, transactions, snapshots, membership, consistent hashing, sharding and fault injection/model checking. Target projects: `chris-raft`, `chris-crdt`, `chris-dist-sim`, `chris-log`, `chris-kv`, `chris-object-store`.

## P2 — breadth that strengthens research depth

### Programming-languages theory and runtime semantics
Operational semantics, type systems, closures, effects, continuations, GC, bytecode and WASM. Target projects: `chris-lang`, `chris-typechecker`, `chris-runtime`, `chris-gc`, `chris-wasm`.

### Advanced cryptography and post-quantum systems
Constant-time engineering, PQC migration, ML-KEM/ML-DSA/SLH-DSA through standards/audited libraries, secret sharing, threshold crypto, commitments, ZK/MPC/FHE concepts. Target projects: `chris-pqc-lab`, `chris-zk-lab`, `chris-mpc-lab`, `chris-crypto-bench`.

### Information theory, coding and DSP
Entropy, source/channel coding, compression, CRC/error correction/erasure concepts, sampling, convolution, FFT and FIR/IIR pipelines. Target projects: `chris-codec-core`, `chris-erasure`, `chris-dsp`, `chris-sdr-sim`.

### Build/release engineering and reproducibility
Cross compilation, sysroots, hermetic/reproducible builds, dependency resolution, package management, CI matrices, artifact provenance/SBOM concepts and release engineering. Target projects: `chris-build`, `chris-package`.

## Cross-cutting research rule

Every advanced track should eventually combine: specification or paper reading -> implementation -> correctness tests -> fuzz/property tests where appropriate -> benchmark/profiling -> explicit hypothesis -> controlled experiment -> limitations -> comparison with a mature reference -> technical write-up.

Coverage breadth is not the goal by itself. Mature projects should converge toward a smaller number of deep systems with real bugs, real measurements, releases and eventually upstream contributions.
