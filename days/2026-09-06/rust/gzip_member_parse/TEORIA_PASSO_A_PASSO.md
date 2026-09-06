# Teoria passo a passo — Gzip member parse (RS-GZ)

## 1. O que estamos construindo

Um **triager/parser estrutural** em Rust para um único member gzip: validar o cabeçalho fixo, navegar campos opcionais sem panic, e ler o trailer. A API devolve um `GzipMemberView` com offsets do stream DEFLATE — você **não** descomprime aqui.

TODOs: `RS-GZ-01` (header fixo), `RS-GZ-02` (início do DEFLATE), `RS-GZ-03` (trailer + view).

## 2. Por que parse estrutural antes de inflate

Gunzip em produção (Node `zlib`, `DeflateStream`) esconde o layout. Em incident response e em toolchains low-level, você precisa:

- rejeitar magic errada antes de alocar;
- respeitar flags reservadas (RFC: bits 5–7 devem ser zero);
- saber **onde** começa o DEFLATE quando há `FNAME`/`FEXTRA`.

Isso ecoa o validator CLVM do Dia 01 e o triage Python `compressed_blob_triage`.

## 3. Cabeçalho fixo — 10 bytes (`RS-GZ-01`)

```text
offset | size | campo
-------|------|---------------------------
0      | 2    | ID1 ID2 = 1F 8B
2      | 1    | CM = 8 (DEFLATE)
3      | 1    | FLG
4      | 4    | MTIME u32 LE
8      | 1    | XFL
9      | 1    | OS
```

### Flags (bitmask)

| Bit | Nome | Significado |
|-----|------|-------------|
| 0 | FTEXT | texto (hint) |
| 1 | FHCRC | CRC16 do header segue |
| 2 | FEXTRA | campo extra com XLEN |
| 3 | FNAME | nome zero-terminated |
| 4 | FCOMMENT | comentário zero-terminated |
| 5–7 | reserved | **devem ser 0** |

### Como validar
```text
se len < 10 → Truncated
se [0..2] != 1f 8b → BadMagic
se [2] != 8 → BadMethod
se flags & 0xE0 != 0 → ReservedFlags
Ok(flags)
```

### Por quê
Aceitar CM≠8 ou flags reservadas é undefined behavior na prática (decompressors divergem). Truncar sem check causa panic em `data[9]`.

### Trace
```text
build_minimal_member(b"RAW", b"hi")
bytes[0..4] = 1f 8b 08 00
```

## 4. Campos opcionais — achar DEFLATE (`RS-GZ-02`)

Ordem **fixada** pela RFC após o byte 10:

```text
p ← 10
se FEXTRA: ler XLEN u16 LE; p += 2 + XLEN
se FNAME: avançar até 0x00 inclusive
se FCOMMENT: idem
se FHCRC: p += 2
return p   // início do DEFLATE
```

Diagrama com só FNAME=`file.txt\0`:

```text
[0..10 fixed][66 69 6c 65 2e 74 78 74 00][DEFLATE...][CRC32][ISIZE]
             f  i  l  e  .  t  x  t  \0
```

### Por quê a ordem importa
FEXTRA antes de FNAME. Implementar na ordem errada desalinha o parser e o trailer “parece” CRC aleatório.

### Bugs comuns
- Esquecer o byte NUL no skip de string.
- Ler XLEN sem garantir `p+2 <= len`.
- Tratar FNAME como length-prefixed (não é).

## 5. Trailer — CRC32 + ISIZE (`RS-GZ-03`)

```text
... DEFLATE bytes ... | CRC32 u32 LE | ISIZE u32 LE |
                        4 bytes        4 bytes
```

Para **um** member que ocupa o buffer inteiro:

```text
trailer_start ← data.len() - 8
deflate ← [deflate_start, trailer_start)
crc ← le32(data[trailer_start..])
isize ← le32(data[trailer_start+4..])
```

### Por quê
ISIZE é o tamanho original mod 2^32 — útil para sanitizar alocação antes de inflate (cruzar com `max_uncompressed` no lab Python). CRC32 do **plaintext**; neste lab só lemos o campo (a função `crc32_gzip` ajuda fixtures).

### Invariantes
- `data.len() >= deflate_start + 8`
- `trailer_start >= deflate_start`
- Member único: não há segundo header após o trailer neste exercício

## 6. CRC32 local — por que sem crates

`crc32_gzip` usa o polinômio reflected `0xEDB88320` (mesmo do gzip). Zero dependências = `cargo test` offline no lab Windows/CI.

### Trace
```text
crc32_gzip(b"PORTAL") → valor estável; build_minimal_member grava no trailer
parse_member lê de volta o mesmo u32
```

## 7. Relação com outros módulos do dia

| Módulo | Papel |
|--------|--------|
| `tooling/zlib_gzip_containers` | C++ — CMF/FLG zlib + gzip wrappers |
| `nodejs/gunzip_transform` | inflate real + backpressure |
| `redteam/compressed_blob_triage` | magic + limites |
| **este lab** | offsets precisos em Rust seguro |

## 8. Ownership

`parse_member` só **observa** `&[u8]` e devolve índices (`usize`) + inteiros. O caller mantém o buffer; a view não segura lifetime do slice (cópia de offsets). Isso evita lifetimes complicados no starter.

### Por quê índices em vez de `&[u8]`
Ensinar aritmética de parser; o próximo passo natural seria `data[view.deflate_start..view.trailer_start]`.

## 9. Tabela de erros

| Erro | Causa típica |
|------|----------------|
| `Truncated` | buffer curto no header/opcionais |
| `BadMagic` | não é gzip |
| `BadMethod` | CM ≠ 8 |
| `ReservedFlags` | bits 5–7 |
| `BadHeader` | inconsistência ao pular campos |
| `BadTrailer` | menos de 8 bytes após DEFLATE |

## 10. Checkpoint no papel

Desenhe o hex de um member mínimo sem flags (10 + 3 bytes opacos + 8 trailer = 21 bytes). Marque `deflate_start=10` e `trailer_start=13`.

## 11. Segurança

Nunca faça `inflate` sem teto de saída. Este lab para **antes** disso — a disciplina de bounds é o produto.

## 12. Resumo operacional

1. Valide 10 bytes fixos.
2. Pule opcionais na ordem RFC.
3. Trailer = últimos 8 bytes do member.
4. Exponha offsets; não confie em FNAME sem NUL check.

## 13. Próximo passo no portfolio

Portar `parse_member` para um CLI `gzip-triage <file>` que imprime offsets e ISIZE — espelho do `clvm-validator` do Dia 01.
