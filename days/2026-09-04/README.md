# Day 02 — 2026-09-04 — versão pedagógica revisada

**Padrão desta revisão:** cada módulo agora possui starter executável/incompleto, teoria do zero, `PESQUISA_GUIADA.md`, resolução com arquivo/função/código exatos, comandos, saída esperada, testes e debugging. `solutions/` permanece como gabarito final.

O foco de hoje é ligar fundamentos de memória, ML systems e pesquisa algorítmica às novas trilhas de computação quântica e sistema operacional próprio.

## Módulos
1. Systems — arena allocator e alinhamento.
2. AI/ML Systems — tensor, strides, transpose view e matmul.
3. Algorithms — merge sort vs quicksort com instrumentação e distribuições adversariais.
4. Quantum — state-vector, gates H/X/Z, CNOT e Bell state.
5. Operating Systems — compositor RGBA portátil que servirá de referência ao futuro graphics stack do `chris-os`.
6. Debugger — framing binário inicial do futuro `chris-debugger` estilo kernel debugger.
7. Red Team seguro — parser ELF64 defensivo para fixtures/binários próprios.

## Regra de honestidade
O `chris-os` ainda **não é um SO bootável** neste dia e o `chris-debugger` ainda **não possui um kernel stub vivo**. Hoje são implementados componentes portáteis de referência com testes, exatamente para não confundir roadmap com funcionalidade pronta.


## Addendum — stacks gerenciadas e runtimes (04/09)
Novas faixas paralelas adicionadas sem substituir os módulos existentes:
- `dotnet/csharp_span_arraypool`: .NET/C# sênior de produção.
- `dotnet/clr_pe_cli_metadata`: CLR/CLI internals from scratch.
- `nodejs/typescript_stream_backpressure`: Node.js/TypeScript sênior de produção.
- `javascript/bytecode_vm_from_scratch`: JavaScript-like lexer/parser/bytecode/VM do zero.

Essas quatro faixas passam a evoluir em paralelo com Systems, AI/ML, Red Team, OS e demais trilhas.
