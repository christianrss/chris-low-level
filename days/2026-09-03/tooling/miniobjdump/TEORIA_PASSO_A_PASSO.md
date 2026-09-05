# Teoria passo a passo — mini objdump (PE/ELF subset)

## 1. O que estamos construindo

Ferramenta que lê um executável PE (Windows) ou ELF64 (Linux), lista sections e decodifica um subconjunto de `.text` x86-64 — como primeiro estágio de `objdump`, PE-bear ou Ghidra.

## 2. Coordenadas que não podem ser misturadas

```text
file offset  -> posição no arquivo em disco
RVA / VA     -> endereço quando mapeado na memória
```

Confundir as duas quebra o dump de `.text`.

## 3. ELF64 — offsets iniciais

```text
byte 0: 0x7F 'E' 'L' 'F'
e_shoff  @ header+0x28 (8 bytes LE) -> section header table
e_shnum  @ header+0x3C
e_shstrndx -> nomes das sections
```

Cada section header: `sh_name`, `sh_addr`, `sh_offset`, `sh_size`.

## 4. PE — offsets iniciais

```text
byte 0: 'M' 'Z'
e_lfanew @ 0x3C -> assinatura PE\0\0
section table após optional header
```

Section `.text` contém código; `VirtualAddress` e `PointerToRawData` mapeiam RVA ↔ arquivo.

## 5. Leitura little-endian (OBJDUMP-U16-01 / U32-01)

```text
u16 = b0 | (b1 << 8)
u32 = b0 | (b1<<8) | (b2<<16) | (b3<<24)
```

Sempre checar `offset + width <= data.size()`.

## 6. Decoder x86-64 (OBJDUMP-PARSE-01)

Instruções têm tamanho variável. Subconjunto do lab:

```text
48 89 E5    mov rbp, rsp
E8 xx xx xx xx  call rel32
C3          ret
```

Se opcode desconhecido: emitir `db 0xNN` e avançar 1 byte — nunca ler além do buffer.

CALL/JMP rel32:

```text
target = address_next_instruction + signed_disp32
```

## 7. Exemplo numérico u32

Bytes `@offset 0x3C`: `80 00 00 00` → `0x00000080` (128).

## 8. Invariantes

- Magic/signature válidos antes de interpretar tabelas.
- Toda leitura bounds-checked.
- PC do decoder sempre avança (progresso garantido).
- `.text` size não ultrapassa arquivo.

## 9. Complexidade

- Parse de headers: O(seções).
- Decode de `.text` de S bytes: O(S) no pior caso (1 byte por `db`).

## 10. Bugs comuns

- `reinterpret_cast` direto em bytes do arquivo.
- Assumir instrução de tamanho fixo.
- Não tratar PE vs ELF na mesma função sem branch.
- Esquecer alinhamento de section headers.
- Parar o decoder sem avançar PC (loop infinito).

## 11. Comparação com produção

| miniobjdump | objdump / llvm-objdump / Capstone |
|-------------|----------------------------------|
| subset manual | tabelas completas Intel/AMD |
| PE ou ELF básico | relocations, symbols, debug |
| `db` fallback | desconhecido sinalizado com metadados |
| sem xref graph | análise de fluxo completa |

Mesma disciplina: validar formato antes de confiar em ponteiros.

## 12. Passo a passo guiado

1. `read_u16_le` / `read_u32_le`.
2. Detectar ELF vs PE.
3. Enumerar sections; localizar `.text`.
4. Loop decode com fallback `db`.
5. `integration_test.py` contra `test_target`.

## 13. Como saber se está correto

Saída contém `Format: ELF` ou `Format: PE` e section `.text`; arquivo inválido rejeitado.
## 4. ELF64 mínimo

```text
[ ELF header 64B ][ program headers ][ sections... ]
```

## 5. Endianness

x86-64 little-endian: `u32 = b0 | b1<<8 | b2<<16 | b3<<24`.

## 6. Campos úteis

| Campo | Offset típico |
|-------|---------------|
| e_shoff | 0x28 |
| e_shentsize | 0x3A |
| e_shnum | 0x3C |

## 7. Seção .text

`sh_offset` + `sh_size` delimita bytes executáveis para dump hex.

## 8. Invariantes

- Magic `\x7fELF`.
- `EI_CLASS == 2` (64-bit).
- Índices de seção dentro do arquivo.

## 9. Bugs comuns

- Ler multi-byte sem bounds check.
- Confundir file offset com VA.
- Assumir .text sempre índice 1.

## 10. Extensão futura

Símbolos, relocations e `.dynsym` ficam para módulo avançado.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
