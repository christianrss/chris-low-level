# Teoria passo a passo — Red Team — ELF64 entry inspector

## 1. O problema que estamos resolvendo

Antes de desmontar um binário ou correlacionar um sample com IOCs, você precisa ler o **cabeçalho ELF64** de forma defensiva: validar magic, confirmar classe/endianness e extrair campos críticos como `e_machine` e `e_entry`. Este módulo implementa um inspector mínimo em Python — sem `readelf`, sem dependências externas.

Em triage de malware, `e_entry` aponta para `_start`, o primeiro código executável após o loader mapear segmentos. Um entry inesperado (fora de segmentos executáveis, ou em região `.data`) é sinal de packer, stub ou corrupção intencional.

## 2. Layout do ELF64 header

O arquivo começa com 16 bytes de identificação (`e_ident`), seguidos pelos campos fixos do header. Em little-endian (o que este lab exige), os offsets são estáveis:

```text
offset 0:  7F 45 4C 46          magic "\x7fELF"
offset 4:  02                     ELFCLASS64
offset 5:  01                     ELFDATA2LSB (little-endian)
offset 6:  01                     EV_CURRENT
offset 16: e_type    (u16)
offset 18: e_machine (u16)
offset 20: e_version (u32)
offset 24: e_entry   (u64)        ← endereço virtual de _start
offset 32: e_phoff   (u64)
offset 40: e_shoff   (u64)
...
offset 64: fim do ELF header fixo (e_ehsize = 64)
```

### Diagrama mental

```text
[ e_ident 16B ][ e_type ][ e_machine ][ e_version ][ e_entry 8B ][ e_phoff ... ]
  ^0            ^16       ^18           ^20           ^24
```

O starter já fornece `ELF64_OFFSETS` — use essa tabela em vez de números mágicos espalhados no código.

## 3. Validação defensiva (`parse_ident`)

Ordem importa: checar tamanho **antes** de indexar bytes.

| Checagem | Condição | Erro |
|----------|----------|------|
| Truncado | `len(data) < 16` | `ValueError("truncated ident")` |
| Magic | `data[:4] != b"\x7fELF"` | `ValueError("bad magic")` |
| Classe | `data[4] != 2` | `ValueError("not ELF64")` |
| Endian | `data[5] != 1` | `ValueError("not little-endian")` |

Não aceite “quase ELF”: buffer vazio, `NOTELF` ou arquivo truncado devem falhar cedo. Isso evita `IndexError` mascarado e comportamento indefinido em `struct.unpack_from`.

## 4. Extração de campos (`parse_elf64`)

Após validar ident, o header completo precisa de pelo menos 64 bytes. Os quatro campos contíguos a partir de `e_type` empacotam como:

```text
formato "<HHIQ" em offset ELF64_OFFSETS["e_type"]
  H  → e_type     (u16)
  H  → e_machine  (u16)
  I  → e_version  (u32)
  Q  → e_entry    (u64)
```

### Fixture sintética do teste

O teste `make_fixture()` grava:

```text
e_type    = 2   (EXEC)
e_machine = 62  (x86-64)
e_version = 1
e_entry   = 0x401000
```

`parse_elf64` chama `parse_ident` internamente — reutilize, não duplique validação.

## 5. `e_entry` e análise forense

`e_entry` é **endereço virtual**, não offset de arquivo. Para correlacionar com disassembly:

1. Leia program headers em `e_phoff` (extensão futura).
2. Encontre segmento `PT_LOAD` com `p_vaddr <= e_entry < p_vaddr + p_memsz`.
3. Converta: `file_offset = e_entry - p_vaddr + p_offset`.

Neste milestone você só extrai o valor; a correlação com `objdump -d --start-address=0x401000` vem depois.

## 6. Invariantes do laboratório

| Invariante | Significado |
|------------|-------------|
| magic `\x7fELF` | arquivo reconhecido como ELF |
| class 2 + data 1 | ELF64 little-endian apenas |
| header ≥ 64 bytes antes de unpack | sem leitura fora dos limites |
| `e_entry` é u64 | não truncar para 32 bits |
| entrada inválida → `ValueError` | nunca retornar dict parcial em dados ruins |

## 7. Bugs clássicos de estudante

1. **Confundir offset de arquivo com RVA** — `e_entry` não é posição no disco.
2. **Ler `e_entry` em offset 24 sem checar `len(data) >= 64`** — `struct.unpack_from` não valida sozinho de forma amigável.
3. **Endian errado** — usar `">HHIQ"` em binário LE corrompe todos os campos.
4. **Validar magic só em `parse_elf64` e esquecer em `parse_ident`** — testes chamam `parse_ident` isoladamente.
5. **Retornar `e_entry` como `int` negativo** — use o valor unsigned de 64 bits.

## 8. Comparação com ferramentas de produção

| Aspecto | Este lab | `readelf -h` | LIEF / Ghidra |
|---------|----------|--------------|---------------|
| Program/section headers | não | sim | sim |
| Validação defensiva | você implementa | sim | sim |
| Dependências | stdlib | binutils | biblioteca pesada |
| Uso em pipeline CI | leve | precisa binutils | variável |

## 9. Trace manual no papel

Para o fixture com `e_entry = 0x401000`:

```text
bytes[24:32] em LE = 00 10 40 00 00 00 00 00
valor = 0x401000
```

Para `e_machine = 62`:

```text
bytes[18:20] = 3E 00  → 0x003E = 62 (EM_X86_64)
```

## 10. Relação com o portfólio

Este módulo é a versão Day 05 do triage ELF (`elf64_triage` em Day 04). A diferença: aqui você usa tabela de offsets nomeada (`ELF64_OFFSETS`) e separa `parse_ident` de `parse_elf64` — preparando parsers incrementais reutilizáveis em pipelines de análise.

## 11. Perguntas de verificação

Antes de implementar, responda no caderno:

1. Por que `parse_elf64` precisa de 64 bytes e não apenas 16?
2. O que acontece se `e_entry = 0` em um executável real?
3. Por que rejeitar big-endian (`data[5] != 1`) simplifica o lab?
4. Como o teste `test_rejects_bad_magic` prova que você não engole lixo silenciosamente?

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
