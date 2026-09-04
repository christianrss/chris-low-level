# Suggested Day 01 Commit Plan

Do not make one giant "day 1" commit. A stronger history separates tests, features and documentation.

```text
test(vm): define binary-format and execution expectations
feat(vm): implement CLVM loader and interpreter

test(ai): add gradient and autograd checks
feat(ai): implement manual training and scalar autograd

test(disasm): add executable inspection regressions
feat(disasm): decode initial x86-64 instructions

test(cpu): define fetch/decode/execute invariants
feat(cpu): implement tiny CPU core

test(asm): define ABI sum behavior
feat(asm): implement x86-64 System V sum

test(assembler): define exact x86-64 byte encodings
feat(assembler): emit mov-imm64 and core opcodes

test(boot): verify boot image size and signature
feat(boot): generate first 512-byte BIOS sector

test(terminal): define fragmented CSI behavior
feat(terminal): implement incremental ESC/CSI parser

test(http): define fragmented request behavior
feat(http): implement incremental request parser

test(p2p): define duplicate-suppression invariants
feat(p2p): implement deterministic gossip

test(chain): define tamper and PoW validation
feat(chain): implement local toy hash chain

test(driver): define descriptor ownership invariants
feat(driver): implement descriptor-ring simulator

bench(day01): record consolidated baselines
docs(day01): document architecture and research roadmap
```
