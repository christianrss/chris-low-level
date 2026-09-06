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
  triage --> entry[Day05 elf_entry_inspector]
  entry --> capstone[projects/chris-binary-toolkit]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/tooling/miniobjdump` | ELF/PE headers, primeiros opcodes |
| 2 | `2026-09-04/redteam/elf64_triage` | Ehdr + Phdr/Shdr + dynsym + strings |
| 3 | `2026-09-05/redteam/elf_entry_inspector` | `e_entry`, validação byte-a-byte |
| Capstone | `projects/chris-binary-toolkit` | pipeline strings + ELF + YARA-style |

---

## 3. VMs e bytecode

```mermaid
flowchart LR
  clvm[Day01 clvm] --> jsvm[Day02 bytecode_vm]
  jsvm --> branch[Day05 bytecode_branch_vm]
  branch --> capstone[projects/chris-js]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/systems/clvm` | stack VM, loader binário |
| 2 | `2026-09-04/javascript/bytecode_vm_from_scratch` | dispatch loop, stack trace |
| 3 | `2026-09-05/javascript/bytecode_branch_vm` | branches, IP, condicionais |
| Capstone | `projects/chris-js` | VM com branches + testes |

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
  pkg[Day05 distro_pkg] --> capstone[projects/chris-linux-module-lab]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/terminal/ansi_parser` | FSM ESC/CSI |
| 2 | `2026-09-05/linux/pty_ansi_terminal` | SGR, cursor, preparação PTY |
| 3 | `2026-09-05/linux/kernel_module_driver_lab` | char device lifecycle |
| 4 | `2026-09-05/linux/distro_pkg_rootfs` | rootfs mínimo (opcional) |
| Capstone | `projects/chris-linux-module-lab` + VM real com `insmod` |

---

## 6. GPU, .NET e performance

```mermaid
flowchart LR
  gfx[Day01 dual_backend_3d] --> portal[Day06 portal_verlet]
  portal --> vk[Day05 vulkan_states]
  hunt[projects/chris-lantern-hunt]
  clr[Day02 clr_pe] --> cil[Day05 cil_decoder]
  matmul[Day05 tiled_matmul] --> capstone[projects/chris-tensor]
```

| Etapa | Módulo | Conceito |
|-------|--------|----------|
| 1 | `2026-09-03/graphics/dual_backend_3d` | software vs GL |
| 1b | `projects/chris-lantern-hunt` | FPS horror OpenGL (projeto extra opcional) |
| 2 | `2026-09-06/graphics/portal_verlet_physics` | portais stencil + Verlet + esfera |
| 3 | `2026-09-04/os/graphics_reference` | compositor RGBA + dirty-rect + frame pacing |
| 4 | `2026-09-05/graphics/vulkan_d3d12_resource_states` | máquina de estados GPU |
| 5 | `2026-09-05/ai/tiled_matmul_cache` | cache blocking, benchmark |
| Capstone | `projects/chris-tensor` + `projects/chris-gpu-state` |

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
| Capstone | `projects/chris-compress` | CLI encadeada |

---

## Como usar

1. Escolha uma trilha alinhada ao seu objetivo de portfólio.
2. Faça os módulos na ordem — cada um assume vocabulário do anterior.
3. Após cada módulo: porte para `projects/` ([PORTING_GUIDE.md](PORTING_GUIDE.md)).
4. No capstone: integre código de 2+ dias em um único repositório com testes unificados.
5. Documente conclusão em `research/YYYY-MM-DD-<trilha>.md`.
