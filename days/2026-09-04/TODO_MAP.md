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

## algorithms/sorting_research
- `D2-SORT-MERGE-RANGE` — merge de intervalos
- `D2-SORT-MERGE-RECURSE` — mergesort recursivo
- `D2-SORT-PARTITION` — partition Lomuto
- `D2-SORT-QUICK-LOOP` — quicksort tail-recursion friendly

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

## debugger/protocol_v1
- `D2-DBG-APPEND-U16` — serializar uint16 LE
- `D2-DBG-APPEND-U32` — serializar uint32 LE
- `D2-DBG-READ-U16` — ler uint16 LE
- `D2-DBG-READ-U32` — ler uint32 LE
- `D2-DBG-FNV1A` — hash FNV-1a do payload
- `D2-DBG-ENCODE` — montar pacote
- `D2-DBG-DECODE` — validar e decodificar pacote

## redteam/elf64_triage
- `D2-ELF-HEADER` — parser defensivo ELF64
- `D2-ELF-STRINGS` — extrator ASCII seguro

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

**Total:** 11 módulos, 43 TODOs mapeados.
