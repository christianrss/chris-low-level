# Mapa global de TODOs — Day 02

## systems/arena_allocator
- `D2-ARENA-POWER2` — validar potência de dois
- `D2-ARENA-ALIGN-UP` — arredondar offset com alinhamento
- `D2-ARENA-ALLOCATE` — bump pointer com capacity check
- `D2-ARENA-RESET` — reset O(1) da arena

## ai/tensor_strides
- `D2-TENSOR-VIEW-AT` — acesso 2D com strides
- `D2-TENSOR-VIEW` — view contígua sem cópia
- `D2-TENSOR-TRANSPOSE` — transpose zero-copy
- `D2-TENSOR-MATMUL` — matmul i-k-j

## algorithms/blocked_merge_sort
- `D2-BLOCK-MERGE-RUN` — merge de dois runs ordenados
- `D2-BLOCK-SORT-TILE` — sort in-place de um tile
- `D2-BLOCK-PASSES` — passes: sort tiles + merge adjacente
- `D2-BLOCK-IO-STATS` — SortIoStats (comparisons / tile I/O)

## quantum/statevector_intro
- `D2-QSIM-SINGLE` — apply matriz 2×2
- `D2-QSIM-X` — gate X
- `D2-QSIM-H` — gate H normalizado
- `D2-QSIM-Z` — gate Z
- `D2-QSIM-CNOT` — controlled-NOT

## os/graphics_reference
- `D2-GFX-INDEX` — indexação linear com bounds
- `D2-GFX-FILL-RECT` — preenchimento recortado
- `D2-GFX-ALPHA-OVER` — composição alpha
- `D2-GFX-COMPOSE` — stack de layers
- `D2-GFX-DIRTY-RECT` — união AABB de regiões dirty
- `D2-GFX-FRAME-PACE` — recompor só damage + FrameStats

## debugger/protocol_v1
- `D2-DBG-APPEND-U16` — serializar uint16 LE
- `D2-DBG-APPEND-U32` — serializar uint32 LE
- `D2-DBG-READ-U16` — ler uint16 LE
- `D2-DBG-READ-U32` — ler uint32 LE
- `D2-DBG-FNV1A` — hash FNV-1a do payload
- `D2-DBG-ENCODE` — montar pacote
- `D2-DBG-DECODE` — validar e decodificar pacote

## redteam/elf64_triage
- `D2-ELF-HEADER` — parser defensivo ELF64 Ehdr
- `D2-ELF-STRINGS` — extrator ASCII seguro
- `D2-ELF-PHDR` — tabela Elf64_Phdr (type/offset/vaddr/filesz/memsz)
- `D2-ELF-SHDR` — tabela Elf64_Shdr + nomes via shstrndx
- `D2-ELF-DYNSYM` — lista (name, st_value) de .dynsym/.dynstr

## dotnet/csharp_span_arraypool
- `D2-CSHARP-WRITE-HEADER` — frame header LE
- `D2-CSHARP-READ-HEADER` — decode sem alocar
- `D2-CSHARP-RENT-FRAME` — ArrayPool + ownership

## dotnet/clr_pe_cli_metadata
- `D2-CLR-CLI-RVA` — RVA → offset do CLI header
- `D2-CLR-METADATA-RVA` — RVA → offset metadata BSJB

## nodejs/typescript_stream_backpressure
- `D2-NODE-FRAME-LINES` — framing por newline com limite

## javascript/bytecode_vm_from_scratch
- `D2-JS-LEX-NUMBER` — lexer de inteiros
- `D2-JS-LEX-IDENT` — identificadores e keywords
- `D2-JS-STMT-LET` — statement let
- `D2-JS-STMT-PRINT` — statement print
- `D2-JS-PREC-ADD` — nível expression
- `D2-JS-PREC-MUL` — nível term
- `D2-JS-VM-ADD` — opcode Add na stack VM

**Total:** 11 módulos, 48 TODOs mapeados.
