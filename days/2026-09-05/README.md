# Day 03 â€” 2026-09-05

Day 03 continua os dois dias anteriores e inaugura formalmente as trilhas permanentes de **Linux distribution/kernel engineering** e **Vulkan/D3D12 explicit graphics**.

## MÃ³dulos
1. Linux distro â€” pacote prÃ³prio + rootfs reproduzÃ­vel.
2. Linux kernel â€” lifecycle de char device + revisÃ£o de mÃ³dulo real.
3. Systems â€” bitmap page allocator.
4. AI/ML Systems â€” matmul naive + tiled.
5. Red Team seguro â€” ELF64 entry-point inspector.
6. .NET/CLR â€” tiny CIL decoder (nÃ£o executado: SDK .NET ausente).
7. Node.js â€” Transform stream + backpressure observÃ¡vel.
8. JavaScript VM â€” JZ/JMP e controle de fluxo.
9. Graphics â€” resource-state tracker com mapeamento Vulkan/D3D12 + debug shaders.
10. Linux terminal â€” ANSI/CSI parser preparando PTY/TTY.

## Como estudar

1. [`START_HERE.md`](START_HERE.md)
2. Por mÃ³dulo: TEORIA (O quÃª/Como/Por quÃª) â†’ **paper-trace / checkpoint conceitual no papel** â†’ EXERCICIOS â†’ starter â†’ TESTES â†’ RESOLUCAO (sÃ³ se travar)
3. NÃ£o avance ao cÃ³digo sem conseguir explicar o fluxo/estado no papel (igual Dia 06; este dia nÃ£o tem `ATIVIDADES.md` centralizado).

## Honestidade de execuÃ§Ã£o
Vulkan/D3D12 sÃ£o ensinados hoje por um simulador portÃ¡til de estados + shaders fonte; nenhum backend real Ã© declarado como executado. O mÃ³dulo de kernel real Ã© revisÃ£o de fonte; o modelo de lifecycle Ã© o artefato executado. .NET nÃ£o foi executado por ausÃªncia do SDK.

