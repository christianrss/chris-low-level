# Teoria — CLVM v2 strings (N4)

## 1. Por que version=2

CLVM v1 (Dia 01/04) cobre inteiros i32, pilha, memória linear e saltos. Programas JS reais precisam de **texto**. Mudar o layout v1 quebraria exercícios, solutions e o loader C++ já entregue.

Solução: **version bump** — byte `data[4] == 2` isola o novo formato. Labs antigos continuam em v1.

### Por que não estender v1 in-place?

- Checksum v1 cobre só `code`.
- Loader C rejeita version ≠ 1 (correto).
- Testes de integração do Dia 01 permanecem estáveis.

## 2. Visão geral do arquivo v2

```text
┌──────────────────────────────────────────────────────────┐
│ Header 16 B (version=2)                                  │
├──────────────────────────────────────────────────────────┤
│ Code (code_size bytes) — opcodes v1 + novos v2           │
├──────────────────────────────────────────────────────────┤
│ String pool — rodata embutido no .clvm                   │
└──────────────────────────────────────────────────────────┘
```

Analogia: seção `.text` (code) + `.rodata` (pool) num ELF reduzido.

## 3. Header v2 (16 bytes)

Mesmos offsets do v1; apenas `version` muda:

```text
offset | tam | campo
-------|-----|------
0x00   | 4   | magic "CLVM"
0x04   | 1   | version = **2**
0x05   | 1   | flags = 0
0x06   | 2   | entry (u16 LE, offset no **code**)
0x08   | 4   | code_size (u32 LE)
0x0C   | 4   | checksum FNV-1a
0x10   | ... | payload = code || pool
```

`entry` aponta só para o bytecode, nunca para dentro do pool.

## 4. Layout do string pool

Após `code[0 .. code_size-1]`:

```text
u32 count                    ; número de strings (LE)
rep count vezes:
    u32 len                  ; tamanho em bytes UTF-8 (LE)
    u8  bytes[len]           ; payload UTF-8, sem NUL terminador
```

Exemplo pool com `["hi", "bye"]`:

```text
02 00 00 00          count = 2
02 00 00 00  68 69   len=2, "hi"
03 00 00 00  62 79 65   len=3, "bye"
```

Diagrama de offsets (code_size = 4):

```text
file offset:
0x10  code[0..3]
0x14  count (4 B)
0x18  len0 + "hi"
0x1E  len1 + "bye"
```

## 5. Checksum v2 — diferença crítica

| Versão | Payload hasheado |
|--------|------------------|
| v1 | `code` apenas |
| v2 | `code || pool` |

Editar uma string no pool sem recalcular FNV → `checksum mismatch`. Mesma filosofia pedagógica do Dia 01, escopo ampliado.

```python
payload = code + pool
checksum = fnv1a32(payload)
```

## 6. Opcode PRINTS (0x21)

| Campo | Valor |
|-------|-------|
| Opcode | 0x21 |
| Operandos | u16 `index` LE (índice no pool) |
| Efeito pilha | nenhum (não usa stack) |
| Runtime | imprime `pool[index]` + newline |

### Por quê índice u16 e não ponteiro?

Bytecode portável não carrega endereços de memória — só offsets no pool embutido. u16 limita a 65535 strings, suficiente para o lab e alinhado ao operand width do opcode.

Codificação no code:

```text
21 00 00    PRINTS index=0
08          HALT
```

`index >= count` → erro em runtime (`string index OOB`).

## 7. Hello world mínimo

Programa didático:

```text
code:  PRINTS(0) + HALT
pool:  ["hi"]
stdout: hi\n
```

Fluxo:

```text
parse_image → code, strings
run_v2:
  pc=0: op=PRINTS → idx=0 → out.append("hi")
  pc=3: op=HALT → break
  return "hi\n"
```

## 8. Funções do lab Python

| Função | Papel |
|--------|-------|
| `encode_pool(strings)` | serializa count + (len + utf8)* |
| `decode_pool(data, offset)` | lê pool a partir de offset; retorna `(strings, next_offset)` |
| `build_image(code, strings)` | monta header + payload + checksum |
| `parse_image(data)` | valida v2 + checksum; separa code e pool |
| `assemble_hello()` | gera imagem de demonstração |
| `run_v2(data)` | mini-interpreter PRINTS + HALT |

Loader C++ do chris-vm **rejeita** v2 — lab usa Python até milestone dual-load.

## 9. UTF-8 no pool

Strings são `str` Python → `encode("utf-8")` na serialização → `decode("utf-8")` na leitura.

Exemplos:

| Texto | bytes UTF-8 |
|-------|-------------|
| `"hi"` | `68 69` |
| `"café"` | `63 61 66 C3 A9` |
| `"日本"` | multi-byte CJK |

Não há NUL obrigatório; comprimento vem do campo `u32 len`.

## 10. Little-endian em todos os inteiros

`struct.pack("<I", n)` — count e len.  
`struct.pack("<H", idx)` — índice PRINTS.  
Header: `struct.pack("<HII", entry, code_size, checksum)`.

Confundir endianness corrompe pool e índices silenciosamente.

## 11. parse_image passo a passo

1. Verificar magic `CLVM` e `data[4] == 2`.
2. Ler `code_size`, `checksum` do header.
3. `body = data[16:]`.
4. Falhar se `fnv1a32(body) != checksum`.
5. `code = body[:code_size]`.
6. `strings, _ = decode_pool(body, code_size)`.

Se `code_size > len(body)`, decode falha naturalmente (buffer curto).

## 12. decode_pool passo a passo

```text
offset ← argumento inicial (tipicamente code_size)
count ← u32 @ offset; offset += 4
strings ← []
rep count:
    n ← u32 @ offset; offset += 4
    raw ← data[offset : offset+n]; offset += n
    strings.append(raw.decode("utf-8"))
return strings, offset
```

`offset` final útil para verificar que o pool consome exatamente o restante do body.

## 13. Diagrama mental v1 vs v2

```text
v1 .clvm:
  [header v1][code]
  checksum = FNV(code)

v2 .clvm:
  [header v2][code][pool]
  checksum = FNV(code || pool)
  opcode extra: PRINTS → pool[idx]
```

## 14. Opcodes reservados

| Op | Status |
|----|--------|
| 0x21 | PRINTS (implementado neste lab) |
| 0x22 | reservado |
| 0x01–0x13 | opcodes v1 válidos no code |

## 15. Erros comuns

- Checksum só sobre `code` (copiar hábito v1).
- Esquecer `count` no início do pool.
- `decode_pool` com offset 0 em vez de `code_size`.
- PRINTS com u32 em vez de u16 para índice.
- Assumir strings NUL-terminated.

## 16. Índice OOB

PRINTS com índice 5 e pool count=1 → runtime error. Verifier v2 futuro pode pré-validar; este lab checa em `run_v2`.

## 17. entry e code_size

`code_size` **não** inclui o pool. Tamanho total do arquivo:

```text
len(file) = 16 + code_size + len(pool_bytes)
```

## 18. Flags

`flags` deve ser 0 (igual v1). Valores não zero → rejeitar em parser estrito.

## 19. Integração com trilha

| Lab | Relação |
|-----|---------|
| Dia 01 | v1 inteiros — intocado |
| Dia 04 | LOAD/STORE v1 — intocado |
| N1 js2clvm | emite v1 — não gera v2 ainda |
| N2 verifier | valida v1 — intocado |
| N4 (este) | introduz v2 + pool |

## 20. Como testar

```powershell
cd solutions   # ou starter após TODOs
python tests/integration_test.py
```

Esperado: gera `hello_v2.clvm`, stdout `hi`.

Depuração: hexdump do arquivo — confirme `data[4]==2`, checksum, pool após code.

## 21. Trace encode_pool(["hi"])

```text
count = 1           → 01 00 00 00
len("hi") = 2       → 02 00 00 00
bytes "hi"          → 68 69
pool total          → 01 00 00 00 02 00 00 00 68 69
```

## 22. Trace decode_pool no offset code_size

Com code de 4 bytes e pool acima:

```text
offset=4: count=1
offset=8: len=2
offset=12: raw=68 69 → "hi"
offset=14: fim pool
```

## 23. build_image end-to-end

```text
pool = encode_pool(["hi"])
payload = code + pool
checksum = fnv1a32(payload)
header = b"CLVM" + bytes([2,0]) + pack("<HII", 0, len(code), checksum)
return header + payload
```

## 24. Mini runner run_v2

Suporta apenas `PRINTS` e `HALT` — suficiente para o lab. Outros opcodes → `unsupported op`. Extensível depois para aritmética v1 no mesmo code.

## 25. Comparação ELF rodata

| ELF | CLVM v2 |
|-----|---------|
| .text | code |
| .rodata | string pool |
| shstrtab indices | u16 index em PRINTS |
| link edit | re-encode pool + checksum |

## 26. Extensibilidade futura

- Dual-load no loader C++.
- js2clvm emitindo v2 para literais string.
- Verifier v2 (bounds de índice PRINTS).
- Heap dinâmico **não** neste lab.

## 27. Checklist mental

1. `version == 2`?
2. Checksum cobre code **e** pool?
3. `decode_pool` começa em `code_size`?
4. PRINTS usa u16 LE?
5. UTF-8 round-trip preserva texto?

## 28. Documentação de referência

`projects/chris-vm/docs/FORMAT_v2.md` — resumo experimental. Este lab é a fonte didática completa.

## 29. Não toque

- `days/2026-09-03` (Dia 01)
- Loader C v1-only
- Solutions v1 existentes

## 30. Síntese

CLVM v2 adiciona **rodata de strings** ao formato binário sem invalidar v1. Você implementa serialização do pool, checksum ampliado e o opcode `PRINTS` — primeiro passo para programas com texto real.
