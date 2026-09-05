# Teoria passo a passo — ELF64 e extração de strings

## 1. ELF em uma frase

ELF (Executable and Linkable Format) descreve como executáveis, objetos e bibliotecas compartilhadas são representados em disco e carregados em memória. Triagem defensiva começa pelo header: magic, ISA, pontos de entrada e offsets de tabelas.

## 2. Identificação — e_ident

Os primeiros 16 bytes são `e_ident`:

```text
offset  campo
0..3    magic 7F 45 4C 46 ("\x7fELF")
4       class (1=32-bit, 2=64-bit)
5       data  (1=LE, 2=BE)
6       version ident
7..15   padding/OSABI
```

Nosso parser aceita **ELFCLASS64 little-endian** apenas — subset deliberado.

## 3. Header de 64 bytes — campos usados

| Offset | Tamanho | Campo | Uso na triagem |
|-------:|--------:|-------|----------------|
| 18 | 2 | e_machine | ISA (62=x86-64) |
| 24 | 8 | e_entry | endereço de _start |
| 32 | 8 | e_phoff | program headers |
| 40 | 8 | e_shoff | section headers |
| 56 | 2 | e_phnum | contagem PH |
| 60 | 2 | e_shnum | contagem SH |
| 62 | 2 | e_shstrndx | índice da string table |

## 4. Diagrama de leitura

```text
[ e_ident 16B ][ resto do ELF64 header ]
        |                |
   validar magic     struct.unpack_from("<H"/"<Q")
   class/endian
```

## 5. Exemplo manual do fixture de teste

Bytes sintéticos do teste esperam:

```text
machine = 62        (EM_X86_64)
entry   = 0x401000
phnum   = 3
shnum   = 12
shstrndx = 11
```

Qualquer offset errado em `unpack_from` quebra um campo isolado — use hex dump para depurar.

## 6. Strings ASCII — algoritmo

Percorra `data + b"\x00"` (sentinela força fechamento no fim):

```text
para cada byte:
  se 0x20 <= byte <= 0x7E -> continua run
  senão -> fecha run se len >= minimum
```

### Exemplo

```text
bytes: 48 65 6C 6C 6F 00 41 42
       H  e  l  l  o     A  B
runs (min=4): offset 0 "Hello"
runs (min=2): "Hello", offset 6 "AB" (se A,B contíguos imprimíveis)
```

## 7. Invariantes do parser

| Invariante | Ação se violado |
|------------|-----------------|
| `len(data) >= 64` | ValueError truncated |
| magic ELF | ValueError mismatch |
| class == 2 | só 64-bit |
| data == 1 | só LE |
| offsets dentro do buffer | futuras fases |

## 8. Bugs clássicos

1. **Offset errado na tabela ELF** (copiar de diagrama 32-bit).
2. **Endianness errada** (`>` em vez de `<`).
3. **Strings sem sentinela NUL** (última run não fecha).
4. **Confundir `minimum` com encoding** (UTF-8 multibyte não é ASCII).
5. **Concluir malware só por string** ("/bin/sh" pode ser falso positivo).

## 9. Comparação com produção

| Ferramenta | Escopo | Nosso lab |
|------------|--------|-----------|
| readelf | completo | header subset |
| objdump | símbolos+reloc | não |
| strings(1) | scan otimizado | pedagogico |
| YARA | assinaturas | regra separada no módulo |
| Binary Ninja | IR completo | triagem inicial |

Triagem real combina header, seções, imports, entropia e regras — strings é só uma lente.

## 10. Limitações conscientes

- Não parseamos program/section headers completos ainda.
- Não validamos checksum do ELF.
- Não suportamos ELF32 nem big-endian.
- Strings não provam comportamento.

## 11. Workflow de análise (lab)

```text
1. parse_elf64_header -> ISA, entry, offsets
2. ascii_strings -> IOCs candidatos
3. comparar com readelf em binário benigno compilado localmente
4. cruzar com YARA (lab_target.yar)
```

## 12. Segurança operacional

Compile apenas `lab_target.c` fornecido. Não execute binários desconhecidos. Strings podem conter dados sensíveis — trate logs como confidenciais.

## 13. Relação red team / blue team

Red team usa strings para encontrar credenciais hardcoded, paths e comandos. Blue team sabe que ofuscação e criptografia reduzem esse sinal. O exercício treina **parser correto**, não conclusões apressadas.

## 14. Perguntas de verificação

1. Qual diferença entre `e_phoff` e `e_shoff`?
2. Por que adicionamos `b"\x00"` no scanner?
3. O que significa `machine=62`?

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
