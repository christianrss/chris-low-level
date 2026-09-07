# Learning paths — trilhas verticais multi-dia

Módulos dentro de um dia são independentes. Estas trilhas conectam conceitos entre dias e terminam em **capstones** em `projects/`.

---

## 1. Memória e alocação

```mermaid
flowchart LR
  arena[Day02 arena_allocator] --> tensor[Day02 tensor_strides]
  tensor --> bitmap[Day05 bitmap_page_allocator]
  bitmap --> capstone[projects/chris-pagealloc]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-04/systems/arena_allocator` | bump pointer, align, reset O(1) |
| 2 | `2026-09-04/ai/tensor_strides` | layout contínuo, views sem cópia |
| 3 | `2026-09-05/systems/bitmap_page_allocator` | page→byte→bit, first-fit |
| Capstone | `projects/chris-pagealloc` | allocator com trace + testes OOM |

**Pergunta de síntese:** quando arena perde para bitmap e vice-versa?

---

## 2. Binários, ELF e reversing

```mermaid
flowchart LR
  mini[Day01 miniobjdump] --> triage[Day02 elf64_triage]
  triage -->   entry[Day05 elf_entry_inspector]
  entry --> hidfuzz[Day07 hid_report_fuzz]
  hidfuzz --> capstone[projects/chris-binary-toolkit]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/tooling/miniobjdump` | ELF/PE headers, primeiros opcodes |
| 2 | `2026-09-04/redteam/elf64_triage` | Ehdr + Phdr/Shdr + dynsym + strings |
| 3 | `2026-09-05/redteam/elf_entry_inspector` | `e_entry`, validação byte-a-byte |
| 4 | `2026-09-06/redteam/compressed_blob_triage` | blobs comprimidos → triage |
| 5 | `2026-09-07/redteam/hid_report_fuzz` | HID boot malformado → bounds no parser N5 |
| Capstone | `projects/chris-binary-toolkit` | pipeline strings + ELF + YARA-style + HID fuzz |

---

## 3. VMs e bytecode

### 3a. CLVM (formato próprio → frontend JS)

```mermaid
flowchart LR
  d1[Day01_clvm] --> d4[Day04_clvm_extended]
  d4 --> cap[chris_vm_js2clvm]
  cap --> n1[Day07_js_codegen]
  n1 --> n2[Day07_verifier]
  n2 --> n3[subset_mod]
  n3 --> n4[Day07_v2_strings]
  n4 --> n7[Day07_rust_v2_verify]
  kmod --> n5[Day07_hid_keyboard]
  n5 --> n6[Day07_ps2_mouse]
  n5 --> n8[Day07_dotnet_input]
  n6 --> n8
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/systems/clvm` | loader, stack VM, JMP/JZ; assembler como IR legível |
| 2 | `2026-09-04/systems/clvm_extended` | CALL/RET, mem, EQ/LT/JNZ |
| Capstone | `projects/chris-vm` | ISA + **`js2clvm`** + checklist N0 |
| N1 | `2026-09-07/systems/clvm_js_codegen` | você implementa codegen (LET/WHILE/CALL) |
| N2 | `2026-09-07/systems/clvm_bytecode_verifier` | stack-effect + branch bounds |
| N3 | chris-vm `%` + `N3_SUBSET_MOD.md` | extensão subset ainda v1 |
| N4 | `2026-09-07/systems/clvm_v2_strings` | FORMAT **v2** strings (Dia01 intocado) |
| N7 | `2026-09-07/rust/clvm_v2_verify` | parser/verifier v2 em Rust |

Estude o capstone com `TEORIA` / `RESOLUCAO_GUIADA` / `docs/STUDY_CHECKLIST_N0.md`.

### 3b. JavaScript-like VM (trilha paralela)

```mermaid
flowchart LR
  jsvm[Day02_bytecode_vm] --> branch[Day05_bytecode_branch_vm]
  branch --> capjs[projects_chris_js]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-04/javascript/bytecode_vm_from_scratch` | dispatch loop, stack trace |
| 2 | `2026-09-05/javascript/bytecode_branch_vm` | branches, IP, condicionais |
| Capstone | `projects/chris-js` | VM com branches + testes (bytecode **próprio**, não CLVM) |

**Perguntas de síntese:** (1) o que CALL/RET na CLVM e um call frame na JS VM têm em comum? (2) por que existem duas VMs (chris-vm vs chris-js)? quando faria sentido **retargetar** o frontend JS para emitir CLVM em vez de opcodes chris-js?
---

## 4. Streams, I/O e backpressure

```mermaid
flowchart LR
  http[Day01 http_parser] --> node[Day02 TS streams]
  node --> bp[Day05 backpressure]
  bp --> capstone[projects/chris-node-streaming]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/network/http_parser` | parsing incremental, estados |
| 2 | `2026-09-04/nodejs/typescript_stream_backpressure` | Transform, `write()` false |
| 3 | `2026-09-05/nodejs/stream_transform_backpressure` | demo observável de backpressure |
| Capstone | `projects/chris-node-streaming` | pipeline com métricas de buffer |

---

## 5. Linux: userspace → kernel

```mermaid
flowchart LR
  ansi[Day01 ansi_parser] --> pty[Day05 pty_ansi]
  pty --> kmod[Day05 kernel_module]
  kmod --> hid[Day07 hid_keyboard]
  hid --> mouse[Day07 ps2_mouse]
  hid --> dotnet_in[Day07 input_event_span]
  pkg[Day05 distro_pkg] --> capstone[projects/chris-linux-module-lab]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/terminal/ansi_parser` | FSM ESC/CSI |
| 2 | `2026-09-05/linux/pty_ansi_terminal` | SGR, cursor, preparação PTY |
| 3 | `2026-09-05/linux/kernel_module_driver_lab` | char device lifecycle |
| 4 | `2026-09-07/linux/hid_keyboard_boot` | HID boot → InputEvent → ring/read |
| 5 | `2026-09-07/linux/ps2_mouse_input` | pacote PS/2 → REL_X/REL_Y |
| 6 | `2026-09-07/dotnet/input_event_span` | struct evdev 24B + Span parsers |
| 7 | `2026-09-05/linux/distro_pkg_rootfs` | rootfs mínimo (opcional) |
| Capstone | `projects/chris-driver-lab` + `chris-linux-module-lab` | fila de input + módulo real |

---

## 6. GPU, .NET e performance

```mermaid
flowchart LR
  d01[Day01 dual_backend_3d gold+depth]
  art[Day07 artillery_2d N9]
  depth[Day07 raster_depth N10]
  ref[Day04 graphics_reference]
  rope[Day06 verlet_rope_3d]
  vk[Day05 vulkan_states]
  d01 --> art
  d01 --> depth
  art --> vk
  art --> ref
  depth --> rope
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/graphics/dual_backend_3d` | software vs GL (+ D3D11 extensão) |
| 2 | `2026-09-07/graphics/artillery_trajectory_2d` | física 2D + CPU/GL/D3D11 |
| 3 | `2026-09-07/graphics/raster_depth_parity` | Z-buffer CPU + paridade GL |
| 4 | `2026-09-04/os/graphics_reference` | compositor RGBA + dirty-rect |
| 5 | `2026-09-06/graphics/verlet_rope_3d` | Verlet 3D + wireframe CPU/GL + orbit camera |
| 6 | `2026-09-05/graphics/vulkan_d3d12_resource_states` | estados GPU + frame graph |
| 1b | `projects/chris-lantern-hunt` | FPS horror OpenGL (opcional) |
| 5b | `2026-09-05/ai/tiled_matmul_cache` | cache blocking, benchmark |
| Capstone | `projects/chris-tensor` + `projects/chris-gpu-state` + `projects/chris-artillery-2d` |

---

## 7. Compressão e formatos de arquivo

```mermaid
flowchart LR
  rle[Day06 rle] --> huf[Day06 huffman]
  huf --> lz[Day06 lz77]
  lz --> defl[Day06 deflate]
  defl --> zlib[Day06 zlib_gzip]
  zlib --> png[Day06 png_idat]
  png --> cap[projects/chris-compress]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-06/systems/rle_byte_codec` | runs byte-a-byte |
| 2 | `2026-09-06/systems/huffman_entropy` | entropia, árvore canônica |
| 3 | `2026-09-06/systems/lz77_dictionary` | janela deslizante |
| 4 | `2026-09-06/systems/deflate_blocks` | RFC 1951 subset |
| 5 | `2026-09-06/tooling/zlib_gzip_containers` | wrappers zlib/gzip |
| 6 | `2026-09-06/tooling/png_idat_pipeline` | chunks PNG + IDAT |
| 7 | `2026-09-06/redteam/compressed_blob_triage` | magic bytes, limites, strings |
| 8 | `2026-09-06/dotnet/span_deflate_buffers` | Span + inflate stored |
| 9 | `2026-09-06/rust/rle_byte_codec` | CHRLE em Rust |
| 10 | `2026-09-06/rust/gzip_member_parse` | header gzip sem panic |
| Capstone | `projects/chris-compress` | CLI encadeada |

---

## 8. Quantum — statevector e medição

```mermaid
flowchart LR
  sv[Day04 statevector_intro] --> meas[Day07 measurement_born]
  meas --> cap[projects/chris-qsim]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-04/quantum/statevector_intro` | gates H, X, CNOT; amplitudes |
| 2 | `2026-09-07/quantum/measurement_born` | medição projetiva, colapso, Born |
| Capstone | `projects/chris-qsim` | simulador 2-qubit + testes de probabilidade |

**Pergunta de síntese:** por que medir |+⟩ em base computacional dá 50/50?

---

## 9. AI — entropia em streams de input

```mermaid
flowchart LR
  tensor[Day06 tensor_entropy_lab] --> evt[Day07 input_event_entropy]
  hid[Day07 hid_keyboard] --> evt
  evt --> cap[projects/chris-tensor]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-06/ai/tensor_entropy_lab` | Shannon, RLE, gzip ratio em tensor |
| 2 | `2026-09-07/ai/input_event_entropy` | mesmas métricas em bytes de InputEvent |
| Capstone | `projects/chris-tensor` | benchmarks + layouts contínuos |

---

## 10. Node.js — Transform de eventos de input

```mermaid
flowchart LR
  gunzip[Day06 gunzip_transform] --> input[Day07 input_event_transform]
  dotnet[Day07 input_event_span] --> input
  input --> cap[projects/chris-node-streaming]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-06/nodejs/gunzip_transform` | Transform, flush, backpressure |
| 2 | `2026-09-07/nodejs/input_event_transform` | records 24B, buffer parcial, métricas |
| Capstone | `projects/chris-node-streaming` | pipeline com métricas de buffer |

---

## Como usar

1. Escolha uma trilha alinhada ao seu objetivo de portfólio.
2. Faça os módulos na ordem — cada um assume vocabulário do anterior.
3. Após cada módulo: porte para `projects/` ([PORTING_GUIDE.md](PORTING_GUIDE.md)).
4. No capstone: integre código de 2+ dias em um único repositório com testes unificados.
5. Documente conclusão em `research/YYYY-MM-DD-<trilha>.md`.
