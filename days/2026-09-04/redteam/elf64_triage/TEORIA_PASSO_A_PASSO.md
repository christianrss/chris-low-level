# Teoria passo a passo — ELF64 triage (Ehdr → Phdr → Shdr → Dynsym)

## 1. ELF em uma frase

ELF (Executable and Linkable Format) descreve como executáveis e bibliotecas são representados em disco e mapeados em memória. Triagem defensiva sobe em camadas: identificar o arquivo → segmentos de carga → seções nomeadas → símbolos dinâmicos — sempre em fixtures/lab targets próprios, sem malware.

### O quê

Parsers pedagógicos em cascata:

1. `parse_elf64_header` — subset ELFCLASS64 little-endian
2. `parse_program_headers` — tabela `Elf64_Phdr` (56 B)
3. `parse_section_headers` — tabela `Elf64_Shdr` (64 B) + nomes via `shstrndx`
4. `list_dynamic_symbols` — `.dynsym` + `.dynstr` → `(name, st_value)`
5. `extract_ascii_strings` — runs imprimíveis `0x20..0x7E`

### Como

Validar `e_ident` → ler offsets do Ehdr → indexar tabelas com `struct.unpack_from("<…")` → resolver C-strings nas string tables.

### Por quê

Header sozinho não mostra o que o loader mapeia nem quais símbolos dinâmicos existem. Phdr/Shdr/Dynsym fecham a lente de triagem inicial **sem** desassemblar nem executar.

## 2. Identificação — e_ident

```text
offset  campo
0..3    magic 7F 45 4C 46 ("\x7fELF")
4       class (1=32-bit, 2=64-bit)
5       data  (1=LE, 2=BE)
6       version ident
7..15   OSABI / padding
```

Este lab aceita **somente** ELFCLASS64 + little-endian — subset deliberado para offsets fixos.

## 3. Elf64_Ehdr — campos usados (64 bytes)

| Offset | Tamanho | Campo | Uso na triagem |
|-------:|--------:|-------|----------------|
| 18 | 2 | e_machine | ISA (62 = EM_X86_64) |
| 24 | 8 | e_entry | VA de entrada |
| 32 | 8 | e_phoff | início da tabela Phdr |
| 40 | 8 | e_shoff | início da tabela Shdr |
| 54 | 2 | e_phentsize | deve ser 56 neste lab |
| 56 | 2 | e_phnum | contagem Phdr |
| 58 | 2 | e_shentsize | deve ser 64 neste lab |
| 60 | 2 | e_shnum | contagem Shdr |
| 62 | 2 | e_shstrndx | índice da seção `.shstrtab` |

## 4. Elf64_Phdr — tabela de program headers (56 bytes cada)

### O quê

Cada entrada descreve um **segmento** que o loader pode mapear (ex.: `PT_LOAD`). Triagem lê type, file offset, VA, tamanho em arquivo e tamanho em memória.

### Como — tabela de offsets relativos ao início da entrada

| Offset | Tipo | Campo | Significado |
|-------:|------|-------|-------------|
| 0 | `<I` | p_type | tipo (1 = PT_LOAD) |
| 4 | `<I` | p_flags | R/W/X (não exigido no parser mínimo) |
| 8 | `<Q` | p_offset | offset no arquivo |
| 16 | `<Q` | p_vaddr | endereço virtual |
| 24 | `<Q` | p_paddr | físico (raro em userland) |
| 32 | `<Q` | p_filesz | bytes no arquivo |
| 40 | `<Q` | p_memsz | bytes em memória (≥ filesz se BSS) |
| 48 | `<Q` | p_align | alinhamento |

Leitura: `base = phoff + i * 56`. Validar `phoff + phnum * 56 ≤ len(data)`.

### Por quê

`memsz > filesz` indica preenchimento zero (BSS). Segmentos anômalos (offset fora do arquivo, type estranho) são sinais de triagem — não prova de malware.

```text
[ Ehdr 64B ][ Phdr0 56B ][ Phdr1 56B ] ...
     |            ^
  e_phoff --------+
```

## 5. Elf64_Shdr — tabela de section headers (64 bytes cada)

### O quê

Seções nomeadas (`.dynsym`, `.dynstr`, `.text`, …) usadas por linkers e ferramentas. Triagem precisa do **nome** além de type/offset/size.

### Como — offsets relativos

| Offset | Tipo | Campo | Significado |
|-------:|------|-------|-------------|
| 0 | `<I` | sh_name | índice em `.shstrtab` |
| 4 | `<I` | sh_type | 0=NULL, 3=STRTAB, 11=DYNSYM, … |
| 8 | `<Q` | sh_flags | alocável etc. |
| 16 | `<Q` | sh_addr | VA (se carregada) |
| 24 | `<Q` | sh_offset | offset no arquivo |
| 32 | `<Q` | sh_size | tamanho |
| 40 | `<I` | sh_link | link (dynsym → dynstr) |
| 56 | `<Q` | sh_entsize | tamanho do elemento (24 p/ Sym) |

Resolver nomes:

```text
shstr = sections[e_shstrndx]
nome  = C-string em data[shstr.offset + sh_name]
```

Alternativa pedagógica: se `shstrndx` falhar, varrer bytes de cada seção candidata por substrings `.dynsym` / `.dynstr` — o lab preferencial usa `shstrndx`.

### Por quê

Sem nomes, `SHT_DYNSYM` ainda ajuda, mas binários stripped/renomeados exigem cruzar type + conteúdo. String table correta evita achar a seção errada.

```text
Shdr table @ e_shoff
   |
   +--> [0] SHT_NULL
   +--> [1] .dynsym  (type 11) -----> bytes @ sh_offset
   +--> [2] .dynstr  (type 3)  -----> "\0lab_main\0"
   +--> [3] .shstrtab (type 3) -----> "\0.dynsym\0.dynstr\0..."
                ^
           e_shstrndx
```

## 6. Elf64_Sym — símbolos dinâmicos (24 bytes)

### O quê

Lista `(name, st_value)` de `.dynsym`, com nomes em `.dynstr`. Triagem benigna: inventário de exports/imports dinâmicos do fixture.

### Como

| Offset | Tipo | Campo |
|-------:|------|-------|
| 0 | `<I` | st_name (índice em dynstr) |
| 4 | `B` | st_info |
| 5 | `B` | st_other |
| 6 | `<H` | st_shndx |
| 8 | `<Q` | st_value |
| 16 | `<Q` | st_size |

`name = C-string(dynstr.offset + st_name)`. Entrada nula (`st_name == 0`) é ignorada na listagem pedagógica.

### Por quê

Símbolos dão âncoras nomeadas para o relatório de triagem (ex.: `lab_main @ 0x401100`) sem precisar de desassembler. Não implica comportamento malicioso.

## 7. Fixture sintético do teste

Layout compacto e benigno:

```text
0x000  Ehdr (phoff=64, phnum=1, shoff=0x200, shnum=4, shstrndx=3)
0x040  Phdr PT_LOAD vaddr=0x400000 filesz=memsz=len(blob)
0x100  .dynsym  — 1 × Elf64_Sym (st_name=1, st_value=0x401100)
0x120  .dynstr  — "\0lab_main\0"
0x140  .shstrtab — "\0.dynsym\0.dynstr\0.shstrtab\0"
0x200  Shdr[4]
```

Esperado: um PHDR `type=1`, seções `.dynsym`/`.dynstr` resolvidas, símbolo `lab_main`.

## 8. Strings ASCII — algoritmo

### O quê

Lista `(offset, text)` de runs ASCII longas o bastante.

### Como

Percorra `data + b"\x00"`; feche run em byte fora de `0x20..0x7E`; filtre por `minimum`.

### Por quê

Complementa símbolos: paths e mensagens aparecem em strings mesmo sem dynsym. Sentinela NUL evita perder a última run.

## 9. Invariantes defensivas

| Invariante | Se violado |
|------------|------------|
| `len >= 64` + magic/class/endian/version | ValueError no Ehdr |
| `phoff + phnum*56 ≤ len` | Phdr truncado |
| `shoff + shnum*64 ≤ len` | Shdr truncado |
| `shstrndx < shnum` | índice inválido |
| `dynsym.size % 24 == 0` | tabela corrompida |
| offsets de string tables dentro do buffer | truncamento |

## 10. Bugs clássicos

1. Usar offsets de **Elf32_Phdr/Shdr** (tamanhos e campos diferentes).
2. Endian `>` em host little-endian.
3. Esquecer que `sh_name` é índice na **shstrtab**, não offset absoluto no arquivo.
4. Confundir `p_vaddr` com file offset ao achar seções.
5. Tratar string/`lab_main` como IOC de malware — neste lab é fixture benigno.
6. Strings sem sentinela NUL no scanner ASCII.

## 11. Comparação com produção

| Ferramenta | Escopo | Nosso lab |
|------------|--------|-----------|
| readelf -l/-S/-s | completo | subset Phdr/Shdr/Dynsym |
| objdump -T | dynsym rico | nome + value |
| eu-readelf | robusto a corruptos | ValueError cedo |
| Binary Ninja | IR | triagem inicial |

## 12. Limitações conscientes

- Sem relocações, `.dynamic`, hash GNU, ou verificação de assinatura.
- Sem ELF32 / big-endian.
- Sem execução do binário.
- Dynsym listado só por nome de seção (ou type DYNSYM + STRTAB).

## 13. Workflow de análise (lab)

```text
1. parse_elf64_header
2. parse_program_headers   -> segmentos
3. parse_section_headers   -> .dynsym/.dynstr
4. list_dynamic_symbols    -> (name, value)
5. extract_ascii_strings   -> IOCs candidatos
6. opcional: readelf no lab_target.c compilado localmente
```

## 14. Segurança operacional

Compile apenas `lab_target.c` fornecido. Não execute binários desconhecidos. Fixtures são sintéticos e benignos. Logs de strings podem conter dados sensíveis de amostras autorizadas — trate como confidenciais.

## 15. Red team / blue team

Red team usa dynsym/strings para achar APIs e paths. Blue team sabe que strip, packing e nomes falsos degradam o sinal. O exercício treina **parser correto**, não veredito de malware.

## 16. Perguntas de verificação

1. Qual a diferença entre `p_filesz` e `p_memsz`?
2. Como `e_shstrndx` conecta `sh_name` ao texto `.dynsym`?
3. Por que `Elf64_Sym` tem 24 bytes e onde está `st_value`?
4. Por que validar bounds **antes** de `unpack_from` em loops `phnum`/`shnum`?

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar layout ELF real a decisões de implementação verificáveis — Ehdr sozinho é insuficiente para triagem séria.

### Por quê estas invariantes?
Cada `TODO [ID]` protege truncamento, índice inválido ou parsing parcial que falha silenciosamente em produção.

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-binary-toolkit` consolida o toolkit com testes e benchmarks reproduzíveis.
