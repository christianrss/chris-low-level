# Roadmap cumulativo - Low-Level Systems

Este laboratório inaugura componentes que serão reutilizados nos próximos treinos.

## Projeto A - CLVM / linguagem / emulador
- Dia 1: formato binário, assembler, loader, stack VM, branches.
- Próximos passos: memória linear, CALL/RET, registradores, syscalls virtuais, debugger próprio, bytecode verifier, JIT simples.
- Evolução: comparar a VM com RV32I e iniciar um emulador RISC-V real.

## Projeto B - Browser
- URL parser -> HTTP -> HTML tokenizer -> DOM -> CSS -> layout -> painting -> compositor -> event loop -> runtime de script.

## Projeto C - Sistema operacional
- boot -> serial -> framebuffer -> allocator -> page tables -> interrupts -> scheduler -> syscalls -> VFS -> drivers -> networking.

## Projeto D - Banco de dados
- page format -> pager -> slotted pages -> B+Tree -> WAL -> transactions -> parser SQL -> executor -> MVCC educacional.

## Projeto E - Engine 3D
- math -> software rasterizer -> camera -> clipping -> z-buffer -> textures -> GPU API -> scene/ECS -> physics -> animation.

## Projeto F - Debugger
- process launch/attach educacional -> breakpoints -> registers -> memory -> symbols -> stack unwinding -> disassembly -> profiler.

## Projeto G - Virtualização
- VM própria -> emulador CPU -> dispositivos virtuais -> RISC-V emulator -> conceitos de hypervisor -> mini VMM educacional.
