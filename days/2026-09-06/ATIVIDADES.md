# ATIVIDADES — 2026-09-06 (fundamentos de compressão + portal + Rust)

**Dia:** 13 módulos | **~24–32 h**  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel). `ctest`/`cargo test` PASS sozinho não basta.

---

## Preparação (30 min)

- [ ] Ler `START_HERE.md` e `README.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-06
```

---

## Bloco 1 — Bits, runs e entropia (4–6 h)

### Objetivo conceitual

Entender **estado de encoder** e **por que** um header com length LE32 permite detectar truncamento.

| Módulo | TODOs | Paper-trace obrigatório |
|--------|-------|-------------------------|
| `systems/rle_byte_codec` | COMP-RLE-01..03 | Hexdump de `AAAAB` → bytes CHRLE |
| `systems/huffman_entropy` | COMP-HUF-01..04 | Freqs `AABBC` → árvore → bitstream MSB |

**Checkpoint conceitual (marque antes do código):**

- [ ] Desenhei no papel os pares `(count,value)` de `AAAAB`
- [ ] Desenhei a árvore Huffman de `AABBC` e o código de cada símbolo
- [ ] Explico em uma frase: MSB-first vs LSB-first

**Depois:** implemente starter; `ctest` solutions deve PASS.

---

## Bloco 2 — Dicionário e blocos (5–7 h)

### Objetivo conceitual

Ver um match LZ77 como referência para trás na janela; ver BTYPE de um bloco DEFLATE no primeiro byte.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/lz77_dictionary` | COMP-LZ77-01..04 | String repetida → tokens (dist,len) |
| `systems/deflate_blocks` | COMP-DEFL-01..05 | Header stored: BFINAL+BTYPE + LEN/NLEN |

**Checkpoint conceitual:**

- [ ] Tracei um match com distância e length no papel
- [ ] Escrevi os bits do primeiro byte de um bloco stored final
- [ ] Sei por que NLEN = ~LEN

---

## Bloco 3 — Wrappers e arquivo (4–6 h)

### Objetivo conceitual

Adler-32 e CRC32 como **assinaturas**; PNG como lista de chunks, não “só pixels”.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `tooling/zlib_gzip_containers` | COMP-ZLIB-01..04 | Adler de string conhecida |
| `tooling/png_idat_pipeline` | COMP-PNG-01..04 | Layout IHDR 13 bytes + CRC do tipo |

**Checkpoint conceitual:**

- [ ] Calculei Adler-32 de uma string curta (tabela s1/s2)
- [ ] Listei ordem: signature → IHDR → IDAT → IEND
- [ ] Sei que IDAT carrega zlib, não pixels crus

---

## Bloco 4 — Portal Verlet (3–4 h)

### Objetivo conceitual

Portal = mudança de **frame**; stencil = máscara de pixels; Verlet = posição a partir da diferença anterior.

| Módulo | TODOs |
|--------|-------|
| `graphics/portal_verlet_physics` | GFX-PORTAL-01..06 |

**Checkpoint conceitual:**

- [ ] Tracei um ponto `(0,0,2)` de A → B no papel
- [ ] Expliquei em 3 passos o stencil (máscara → câmera espelhada → desenhar)

**Checkpoint visual:**

```powershell
cmake -S days/2026-09-06/graphics/portal_verlet_physics/solutions -B build-portal -A x64
cmake --build build-portal --config Release
ctest --test-dir build-portal -C Release
.\build-portal\Release\portal_demo.exe
```

- [ ] Vista através do portal
- [ ] Esfera atravessa A→B

---

## Bloco 5 — Trilhas obrigatórias (6–8 h)

| Módulo | Checkpoint conceitual |
|--------|----------------------|
| `ai/tensor_entropy_lab` | Calculei H de um buffer 2 símbolos iguais |
| `redteam/compressed_blob_triage` | Listei magic `1F 8B` e `78 9C` |
| `dotnet/span_deflate_buffers` | Desenhei BTYPE no nibble do header |
| `nodejs/gunzip_transform` | Expliquei por que `write()===false` importa |

**Gate:**

```powershell
python scripts/run_day_tests.py --day 2026-09-06 --mode solutions
```

---

## Bloco 6 — Rust seguro (3–4 h)

### Objetivo conceitual

Mesmo wire format / RFC, mas com **`Result` + bounds antes de indexar** — ownership como disciplina de trust-boundary.

| Módulo | TODOs | Paper-trace obrigatório |
|--------|-------|-------------------------|
| `rust/rle_byte_codec` | RS-RLE-01..03 | Hexdump de `AAAAB` → frame CHRLE (igual Bloco 1, agora em Rust) |
| `rust/gzip_member_parse` | RS-GZ-01..03 | Layout member: 10 bytes fixos + FNAME opcional + trailer 8 |

**Checkpoint conceitual:**

- [ ] Desenhei no papel `AAAAB` em CHRLE e sei onde está o LE32
- [ ] Listei a ordem RFC dos campos opcionais gzip (FEXTRA → FNAME → FCOMMENT → FHCRC)
- [ ] Explico em uma frase: panic OOB vs `Err(Truncated)`

**Depois:**

```powershell
cargo test --manifest-path days/2026-09-06/rust/rle_byte_codec/solutions/Cargo.toml
cargo test --manifest-path days/2026-09-06/rust/gzip_member_parse/solutions/Cargo.toml
```

---

## Bloco 7 — Capstone (2 h)

- [ ] Portar para `projects/chris-compress/`
- [ ] Preencher Relatório de resolução em cada módulo feito

---

## Checklist final

- [ ] Paper-traces dos blocos 1–4 e 6 feitos
- [ ] pedagogy_check PASS
- [ ] run_day_tests solutions PASS
- [ ] `portal_demo` visto manualmente
- [ ] Rust: `cargo test` solutions PASS nos dois módulos
- [ ] BENCHMARK com Resultados observados

## Extra

`projects/chris-lantern-hunt` — **não** faz parte deste dia.
