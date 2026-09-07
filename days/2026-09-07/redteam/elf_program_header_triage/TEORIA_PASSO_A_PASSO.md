# Teoria passo a passo — ELF64 program headers (D5-ELF)

## 1. O que estamos construindo

Um parser **defensivo** de **program headers** (`Elf64_Phdr`) em Python puro: valida cabeçalho ELF64 little-endian, localiza a tabela PHDR, decodifica campos e rejeita ranges impossíveis. Fixture sintético em memória — **não executamos** o binário.

TODOs: `D5-ELF-HEADER` (magic + localizar tabela), `D5-ELF-PHDR` (decodificar entrada), `D5-ELF-RANGE` (bounds + regra PT_LOAD).

## 2. Por quê program headers antes de sections

**Section headers** descrevem organização para link/edit (`.text`, `.data`, símbolos). **Program headers** descrevem **segmentos carregáveis** — o que o loader mapeia em memória (`PT_LOAD`, `PT_DYNAMIC`, …). Em triage red team, PHDR é onde offsets e tamanhos de segmento entram cedo: parser frágil aqui vira execução de bytes fora do arquivo ou BSS mal modelado.

## 3. Layout ELF64 header (offsets fixos)

```text
offset  campo              tamanho
+0      e_ident            16
+16     e_type, e_machine…  (resto do Ehdr)
+32     e_phoff            u64  ← início da tabela PHDR
+54     e_phentsize        u16  ← tamanho de cada Phdr
+56     e_phnum            u16  ← quantidade de entradas
```

Magic: bytes `7F 45 4C 46` (`"\x7fELF"`). Byte 4 = **class** (2 = ELF64). Byte 5 = **endian** (1 = LE).

| Campo | Por que importa |
|-------|-----------------|
| `e_phoff` | ponteiro para primeira `Elf64_Phdr` |
| `e_phentsize` | stride do loop (≥ 56 para ELF64) |
| `e_phnum` | quantas entradas ler |

## 4. Validação de header (`D5-ELF-HEADER`)

### O quê
Rejeitar blobs que não são ELF64 LE e garantir que a tabela PHDR cabe no buffer antes de indexar.

### Como
1. `len(data) >= 64` (Ehdr mínimo).
2. `data[:4] == b"\x7fELF"`, `data[4] == 2`, `data[5] == 1`.
3. Ler `phoff`, `phentsize`, `phnum` nos offsets acima (little-endian).
4. Exigir `phentsize >= 56` e `phoff + phentsize * phnum <= len(data)`.

### Por quê
Validar **antes** do loop evita `IndexError` silencioso ou leitura de lixo como `p_type`. Stride errado (`phentsize` pequeno) sobrepõe entradas — bug comum em parsers C copy-paste.

### Trace manual — fixture do teste

```text
len=256, phoff=64, phentsize=56, phnum=2
tabela ocupa bytes [64, 64+112) = [64, 176)
176 <= 256  ✓
entrada 0 em off=64, entrada 1 em off=120
```

### Invariantes
- Parser nunca indexa `data[o:o+56]` sem bounds pré-validados.
- ELF32 / big-endian rejeitados cedo (fora do escopo do lab).

### Bugs comuns
- Ler `phnum` no offset errado (confundir com ELF32).
- Esquecer `phentsize >= 56`.
- Validar range de segmento **depois** de append — tarde demais se slice já leu lixo.

## 5. Decodificar Elf64_Phdr (`D5-ELF-PHDR`)

### O quê
Para cada índice `i`, `off = phoff + i * phentsize`, ler campos e montar dict.

### Como — offsets dentro de cada Phdr (ELF64)

```text
+0   p_type    u32
+4   p_flags   u32
+8   p_offset  u64
+16  p_vaddr   u64
+32  p_filesz  u64
+40  p_memsz   u64
+48  p_align   u64
```

Loop:
```text
for i in range(phnum):
    o = phoff + i * phentsize
    decodificar campos → dict(type, flags, offset, vaddr, filesz, memsz, align)
```

### Por quê
Offsets fixos da ABI System V permitem parser sem dependência de `struct` — alinhado a triage manual hex editor. Separar decode de validate deixa testes unitários por camada.

### Trace manual — entrada 0 do fixture

```text
off=64: type=1 (PT_LOAD), flags=5, p_offset=200, filesz=16, memsz=32
bytes file [200, 216) devem existir no buffer de 256 bytes
```

### Invariantes
- Uma entrada por índice; ordem preservada na lista de saída.
- Tipos desconhecidos ainda decodificam — regras extras ficam em RANGE.

### Bugs comuns
- Usar offset +4 para `p_offset` (confundir com ELF32 Phdr).
- `int.from_bytes` sem `"little"`.
- Retornar tupla em vez de dict com chaves esperadas pelo teste.

## 6. Validação de ranges (`D5-ELF-RANGE`)

### O quê
Antes de aceitar cada entrada: segmento não ultrapassa arquivo; `PT_LOAD` respeita `memsz >= filesz`.

### Como
```text
se p_offset + p_filesz > len(data): ValueError("segment outside file")
se p_type == 1 e p_memsz < p_filesz: ValueError("PT_LOAD memsz < filesz")
```

`PT_LOAD` = tipo 1. Bytes `[filesz, memsz)` representam BSS zerado — memória sem backing no arquivo.

### Por quê
`p_filesz > len(file)` é vetor clássico de **parser diferencial** e leitura OOB. `memsz < filesz` é inconsistente: loader copiaria mais bytes do que reserva em memória.

### Trace manual — caso rejeitado pelo teste

```text
mutação: p_offset=250, filesz=16 em buffer len=256
250+16=266 > 256 → ValueError segment outside file
```

### Invariantes
- Range exato terminando em `len(data)` é válido (`==` permitido).
- `filesz=0` permitido se offset dentro do arquivo.

### Bugs comuns
- Validar só primeiro segmento.
- Comparar `memsz` com `len(data)` em vez de `filesz`.
- Ignorar tipo — regra `memsz >= filesz` só para PT_LOAD neste lab.

## 7. Fluxo do parser

```text
bytes ──► HEADER: magic/class/endian + bounds tabela
              │
              ▼
         loop PHDR: decode campos
              │
              ▼
         RANGE: offset+filesz ≤ len; PT_LOAD memsz≥filesz
              │
              ▼
         list[dict]
```

## 8. Tabela de tipos comuns (metadado)

| p_type | Nome | Papel |
|--------|------|-------|
| 1 | PT_LOAD | segmento carregável |
| 4 | PT_NOTE | notas auxiliares |
| 3 | PT_INTERP | interpretador |

Fixture usa PT_LOAD (1) e PT_NOTE (4).

## 9. Complexidade

| Fase | Tempo | Espaço |
|------|-------|--------|
| Header | O(1) | O(1) |
| Loop PHDR | O(phnum) | O(phnum) saída |

## 10. Comparação com produção

| Este lab | Ferramentas reais |
|----------|-------------------|
| Buffer bytes sintético | `readelf -l`, LIEF, pyelftools |
| PT_LOAD bounds | relro, NX, ASLR, validação de align |
| Sem sections | análise de `.dynamic`, reloc |

Transferível: **ordem header → decode → bounds**, não lista completa de tipos ELF.

## 11. Passo a passo guiado

1. `D5-ELF-HEADER` — validação e leitura de `phoff/ents/num`.
2. `D5-ELF-PHDR` — loop de decode.
3. `D5-ELF-RANGE` — checks antes de `append`.
4. `python starter/test_elf_phdr.py` → `chris-elf-phdr tests passed`.

## 12. Como saber se está correto

- Fixture oficial: duas entradas, primeira `type==1`.
- Mutação offset 250 + filesz 16 → `ValueError`.
- Magic `\x7fELF`, class 2, endian 1 obrigatórios.

## 13. Por quê este módulo existe

Treinar **parser defensivo** em formato binário realista — offsets, stride, bounds — antes de emuladores e exploit dev. Cada TODO isola uma falha que em produção vira crash, info leak ou execução de região não mapeada.
