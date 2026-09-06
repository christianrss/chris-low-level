# Day 02 — 2026-09-04 — versão pedagógica revisada

**Padrão desta revisão:** cada módulo agora possui starter executável/incompleto, teoria do zero, `PESQUISA_GUIADA.md`, resolução com arquivo/função/código exatos, comandos, saída esperada, testes e debugging. `solutions/` permanece como gabarito final.

O foco de hoje é ligar fundamentos de memória, ML systems e pesquisa algorítmica às novas trilhas de computação quântica e sistema operacional próprio.

## Módulos
1. Systems — arena allocator e alinhamento.
2. AI/ML Systems — tensor, strides, transpose view e matmul.
3. Algorithms — **blocked merge sort** (tiles + passes + I/O stats) — systems, não CS101.
4. Quantum — state-vector, gates H/X/Z, CNOT e Bell state.
5. Operating Systems — compositor RGBA + **dirty-rect** + **frame pacing** (referência `chris-os`).
6. Debugger — framing binário inicial do futuro `chris-debugger`.
7. Red Team seguro — ELF64 **Ehdr + Phdr + Shdr + dynsym** + strings (fixtures próprias).

## Regra de honestidade
O `chris-os` ainda **não é um SO bootável** neste dia e o `chris-debugger` ainda **não possui um kernel stub vivo**. Hoje são implementados componentes portáteis de referência com testes, exatamente para não confundir roadmap com funcionalidade pronta.


## Addendum — stacks gerenciadas e runtimes (04/09)
Novas faixas paralelas adicionadas sem substituir os módulos existentes:
- `dotnet/csharp_span_arraypool`: .NET/C# sênior de produção.
- `dotnet/clr_pe_cli_metadata`: CLR/CLI internals from scratch.
- `nodejs/typescript_stream_backpressure`: Node.js/TypeScript sênior de produção.
- `javascript/bytecode_vm_from_scratch`: JavaScript-like lexer/parser/bytecode/VM do zero.

Essas quatro faixas passam a evoluir em paralelo com Systems, AI/ML, Red Team, OS e demais trilhas.

## Nota da auditoria final

A versão corrigida do Day 02 usa os arquivos Markdown de cada módulo como fonte pedagógica autoritativa. O DOCX anterior foi removido deste pacote porque havia sido gerado antes da auditoria `starter ↔ resolução ↔ testes ↔ solution` e poderia conter instruções desatualizadas.

Valide a entrega com:

```bash
python scripts/pedagogy_check_day02.py
python scripts/quality_check.py
```
