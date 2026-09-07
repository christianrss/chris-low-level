# Resolução guiada passo a passo — Rust / CLVM v2 verify

Trabalhe em `days/2026-09-07/rust/clvm_v2_verify/starter/`. Ordem sugerida: POOL → HEADER → PRINTS → STACK.

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `CLVM-RS-V2-POOL-02` | `starter/src/lib.rs` | `encode_pool`, `decode_pool` | stubs `TODO [CLVM-RS-V2-POOL-02]` |
| `CLVM-RS-V2-HEADER-01` | `starter/src/lib.rs` | `parse_image` | stub que retorna `Truncated` |
| `CLVM-RS-V2-PRINTS-03` | `starter/src/lib.rs` | `assemble_hello`, `run_prints` | `unimplemented!` |
| `CLVM-RS-V2-STACK-04` | `starter/src/lib.rs` | `verify_stack` | lista stub de erro |

## Baseline

```powershell
cd days/2026-09-07/rust/clvm_v2_verify/starter
cargo test
```

**Esperado:** FAIL — stubs retornam `Truncated`, `unimplemented!`, erro stub em `verify_stack`. Hex de `fixtures/hello_v2.clvm` começa com `43 4C 56 4D 02 00`.

Wire format de referência: `days/2026-09-07/systems/clvm_v2_strings/solutions/clvm_v2.py`.

---

## CLVM-RS-V2-POOL-02 — pool

### Onde colocar (POOL-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Funções | `encode_pool`, `decode_pool` |
| Substituir | corpos vazios com `TODO [CLVM-RS-V2-POOL-02]` |
| Não mexer | `fnv1a32`, `build_image` |

### 1. O problema (POOL-02)

Sem serialização do pool, `parse_image` não separa rodata do bytecode e `PRINTS` não tem strings para indexar.

### Escreva o código (POOL-02)

`encode_pool`: `count u32 LE`, depois para cada string `len u32 LE + bytes UTF-8`.

`decode_pool(data, offset)`: leia count, loop len+bytes, retorne `(strings, pos_final)`; erro `Truncated` se buffer curto ou UTF-8 inválido.

### Por que funciona (POOL-02)

Formato determinístico; `pos` final encadeia após `code` em `parse_image`.

### Verifique (POOL-02)

```powershell
cargo test caso_3_pool_round_trip -- --nocapture
```

---

## CLVM-RS-V2-HEADER-01 — parse_image

### Onde colocar (HEADER-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função | `parse_image` |
| Substituir | stub que sempre retorna `Err(Truncated)` |
| Não mexer | constantes `MAGIC`, `VERSION`, `HEADER_SIZE` |

### 1. O problema (HEADER-01)

Imagem v2 exige validar magic, version=2, checksum FNV sobre `body = data[16..]`, fatiar `code` por `code_size` e chamar `decode_pool(body, code_size)`.

### Escreva o código (HEADER-01)

Valide tamanho ≥ 16, magic, version, checksum com `fnv1a32(body)`, extraia `code = body[..code_size]`, decode pool no offset `code_size`.

### Por que funciona (HEADER-01)

Checksum cobre code+pool; `code_size` não inclui pool.

### Verifique (HEADER-01)

```powershell
cargo test caso_1 caso_2 caso_6 -- --nocapture
```

**Esperado:** hello parse OK; `bad_magic` → `BadMagic`; `bad_checksum` → `ChecksumMismatch`.

### Debug (HEADER-01)

| Sintoma | Causa | Ação |
|---------|-------|------|
| checksum fail em hello | hasheou só code | FNV em `body` inteiro |
| pool vazio | offset 0 em decode | use `code_size` |

---

## CLVM-RS-V2-PRINTS-03 — assemble + run

### Onde colocar (PRINTS-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Funções | `assemble_hello`, `run_prints` |
| Substituir | `unimplemented!` em ambas |
| Não mexer | `build_image`, `parse_image` |

### 1. O problema (PRINTS-03)

Bytecode referencia strings por índice u16; texto vive no pool. `assemble_hello` monta `PRINTS 0; HALT` + pool `["hi"]`; `run_prints` interpreta e junta linhas com `\n`.

### Escreva o código (PRINTS-03)

`assemble_hello`:

```rust
pub fn assemble_hello() -> Vec<u8> {
    let mut code = Vec::with_capacity(4);
    code.push(PRINTS);
    code.extend_from_slice(&0u16.to_le_bytes());
    code.push(HALT);
    build_image(&code, &["hi"])
}
```

`run_prints`: loop em `image.code`, case `PRINTS` lê u16 idx, valida `< strings.len()`, append; `HALT` break; join com `\n` final.

### Por que funciona (PRINTS-03)

Índice u16 aponta para rodata; runner não aloca pool — só lê `ClvmV2Image`.

### Verifique (PRINTS-03)

```powershell
cargo test caso_4_run_prints_stdout -- --nocapture
```

**Esperado:** stdout lógico `"hi\n"`.

### Debug (PRINTS-03)

| Sintoma | Causa | Ação |
|---------|-------|------|
| stdout vazio | idx errado | confira u16 LE após opcode |
| PoolOob | pool vazio | `build_image` com `["hi"]` |

---

## CLVM-RS-V2-STACK-04 — verify_stack

### Onde colocar (STACK-04)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função | `verify_stack` |
| Substituir | stub que retorna erro fixo |
| Não mexer | opcodes `PRINTS`, `HALT` |

### 1. O problema (STACK-04)

Executar bytecode inválido é caro. Walk linear detecta operandos truncados e índice `>= pool_len` antes de `run_prints`.

### Escreva o código (STACK-04)

```rust
pub fn verify_stack(code: &[u8], pool_len: usize) -> Vec<String> {
    let mut errors = Vec::new();
    let mut pc = 0usize;
    while pc < code.len() {
        let start = pc;
        let op = code[pc];
        pc += 1;
        match op {
            HALT => {}
            PRINTS => {
                if pc + 2 > code.len() {
                    errors.push(format!("truncated PRINTS operand at {start}"));
                    break;
                }
                let idx = u16::from_le_bytes([code[pc], code[pc + 1]]) as usize;
                pc += 2;
                if idx >= pool_len {
                    errors.push(format!("pool index OOB {idx} >= {pool_len} at {start}"));
                }
            }
            other => {
                errors.push(format!("unknown opcode 0x{other:02x} at {start}"));
                break;
            }
        }
    }
    errors
}
```

### Por que funciona (STACK-04)

Sem VM — só forma e bounds de índice.

### Verifique (STACK-04)

```powershell
cargo test caso_5_verify_stack_clean_and_oob -- --nocapture
```

**Esperado:** hello → `errors.is_empty()`; idx OOB → mensagem contendo `OOB`.

### Debug (STACK-04)

| Sintoma | Causa | Ação |
|---------|-------|------|
| falso OOB | pool_len errado | passe `strings.len()` |
| truncated não detectado | não checou `pc+2` | bounds antes de ler u16 |

---

## Relatório de resolução

| Campo | Preencher |
|-------|-----------|
| TODOs completados | HEADER-01, POOL-02, PRINTS-03, STACK-04 |
| `cargo test` starter | PASS / FAIL |
| Depuração (hex/offset) | |
| Dúvidas | |

Checklist final:
- [ ] `data[4] == 2`
- [ ] checksum cobre code+pool
- [ ] PRINTS usa u16 LE
- [ ] `verify_stack` vazio para hello

Fim da resolução guiada CLVM v2 Rust.
