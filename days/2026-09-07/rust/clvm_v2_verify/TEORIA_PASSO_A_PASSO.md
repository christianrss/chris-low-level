# Teoria passo a passo — CLVM v2 verify (Rust)

## 1. O que estamos construindo

Parser e mini-runner **CLVM version=2** em Rust, espelhando o wire format do lab Python `systems/clvm_v2_strings/solutions/clvm_v2.py`. Você implementará:

- `parse_image` — valida magic, version byte, checksum FNV-1a sobre `code || pool`
- `encode_pool` / `decode_pool` — rodata de strings UTF-8
- `assemble_hello` / `run_prints` — opcode `PRINTS` (0x21) + `HALT` (0x08)
- `verify_stack` — walk estático (operandos, índice de pool, efeito de pilha 0→0)

TODOs: `CLVM-RS-V2-HEADER-01`, `CLVM-RS-V2-POOL-02`, `CLVM-RS-V2-PRINTS-03`, `CLVM-RS-V2-STACK-04`.

## 2. Por que Rust neste lab?

O Dia 07 já tem o formato v2 em Python. Rust força **bounds checking explícito**, `Result` tipado e slices `&[u8]` — habilidades necessárias para portar o loader para `chris-vm` sem depender do runtime Python.

## 3. Layout da imagem v2

```text
offset | tamanho | campo
-------|---------|---------------------------
0..3   | 4       | magic "CLVM"
4      | 1       | version = 2
5      | 1       | flags (0 no subset)
6..7   | 2       | reserved (0)
8..11  | 4       | code_size (u32 LE)
12..15 | 4       | checksum FNV-1a32(body)
16..   | code_size | bytecode
..     | resto   | string pool
```

Body = `code || pool`. Checksum cobre **code + pool** — editar string sem recalcular FNV deve falhar.

### Por quê checksum sobre code+pool?

v1 hasheia só bytecode. v2 embute rodata no arquivo — alterar uma string sem atualizar FNV deve falhar como corrupção, não como stdout silenciosamente errado.

## 4. String pool

```text
[u32 count][u32 len0][utf8 bytes0][u32 len1][utf8 bytes1]...
```

Sem terminador NUL. Lens little-endian. UTF-8 válido (lab rejeita bytes inválidos como `Truncated`).

### Por quê pool sem NUL?

Comprimento explícito (`u32 len`) permite strings com bytes `0x00` internos e parsing forward-only sem scan — mesmo padrão de seções ELF `.rodata`.

## 5. Opcode PRINTS 0x21

```text
21 | idx u16 LE | ...
```

Em runtime: `out += strings[idx] + "\n"`. `HALT` (0x08) encerra o loop.

Hello world mínimo: `code: 21 00 00 08`, pool: `01 00 00 00 02 00 00 00 68 69`.

## 6. FNV-1a 32-bit

Offset `0x811C9DC5`, prime `0x01000193`, máscara via `u32` wrapping (`wrapping_mul`).

## 7. verify_stack — filosofia

Walk **sem executar**: opcode conhecido, operandos presentes, índice `< pool_len`, profundidade de pilha (PRINTS/HALT: efeito 0,0). Retorna `Vec<String>` de erros — vazio = OK.

### Por quê walk estático antes de run?

`run_prints` aloca `String` e pode falhar tarde com índice OOB. Verifier barato pega formato inválido antes de side effects — mesma filosofia do verifier v1 Python.

## 8. Diagrama mental

```text
[arquivo .clvm]
    → parse_image → ClvmV2Image { code, strings }
    → verify_stack(code, strings.len())
    → run_prints → String stdout
```

## 9. Erros tipados (`ClvmV2Error`)

| Variante | Quando |
|----------|--------|
| `Truncated` | buffer curto |
| `BadMagic` | ≠ "CLVM" |
| `BadVersion` | byte 4 ≠ 2 |
| `ChecksumMismatch` | FNV diverge |
| `PoolOob` | índice em runtime |
| `UnsupportedOpcode` | op desconhecido |
| `TruncatedOperand` | PRINTS sem u16 |

## 10. Helpers já prontos no starter

`fnv1a32`, `build_image` — não altere.

## 11. Fixtures

| Arquivo | Propósito |
|---------|-----------|
| `hello_v2.clvm` | imagem válida PRINTS "hi" |
| `bad_magic.clvm` | primeiro byte corrompido |
| `bad_checksum.clvm` | último byte flipado |

## 12. Relação com labs anteriores

| Lab | Lição |
|-----|-------|
| `clvm_v2_strings` (Python) | wire format canônico |
| `clvm_bytecode_verifier` | walk estático |
| `gzip_member_parse` (Rust) | parsing com slices |

## 13. Invariantes

1. `HEADER_SIZE == 16`.
2. `code_size` não inclui pool.
3. `decode_pool` começa em `code.len()` dentro do body.
4. `run_prints` só aceita `PRINTS` e `HALT`.

## 14. Bugs comuns

- Checksum só sobre `code` (errado).
- Ler `version` em offset errado (v1 usa entry u16 em 6).
- `PRINTS` operand big-endian.
- `verify_stack` esquecer `pc += 2` após u16.

## 15. Depuração

```powershell
cargo test caso_1 -- --nocapture
Format-Hex fixtures\hello_v2.clvm
```

Compare bytes 8..11 com tamanho do segmento code (4 para hello).

## 16. Síntese

Você porta o loader v2 Python para Rust com `Result`, slices e verifier estático — preparação para integração no `chris-vm`.
