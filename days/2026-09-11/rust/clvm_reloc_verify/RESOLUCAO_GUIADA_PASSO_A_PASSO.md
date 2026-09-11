# Resolução guiada — clvm_reloc_verify (Rust)

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `RS-RELOC-01` | `starter/src/lib.rs` | `reloc_table_len` |
| `RS-RELOC-02` | `starter/src/lib.rs` | `reloc_site` |
| `RS-RELOC-03` | `starter/src/lib.rs` | `reloc_sites_in_bounds` |

## Baseline

```powershell
// contexto: substitua o corpo sob o TODO
cargo test --manifest-path days/2026-09-11/rust/clvm_reloc_verify/starter/Cargo.toml
// fim do corpo; preserve a assinatura
```

**Esperado:** FAIL.

## RS-RELOC-01

### Onde colocar (RS-RELOC-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função | `reloc_table_len` |
| Substituir | o corpo sob o comentário `TODO [RS-RELOC-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Precisa Ok(1) para 2 bytes.

### Algoritmo / trace

se len%2!=0 Err; Ok(len/2).

### Escreva o código

```rust
    if bytes.len() % 2 != 0 { return Err("odd"); }
    Ok(bytes.len() / 2)
    // end
```

### Por que funciona?

Cada entrada = 2 bytes.

### Verifique

Ok(1); Err no slice ímpar.

### Código completo alinhado ao solutions/ (RS-RELOC-01)

```rust
PEDAGOGY-SOLUTION: RS-RELOC-01
    if bytes.len() % 2 != 0 { return Err("odd"); }
    Ok(bytes.len() / 2)
}
pub fn reloc_site(bytes: &[u8], index: usize) -> Result<u16, &'static str> {
    // 
```

## RS-RELOC-02

### Onde colocar (RS-RELOC-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função | `reloc_site` |
| Substituir | o corpo sob o comentário `TODO [RS-RELOC-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Índice 1 deve ler 4.

### Algoritmo / trace

from_le_bytes em index*2.

### Escreva o código

```rust
    let n = reloc_table_len(bytes)?;
    if index >= n { return Err("oob"); }
    let i = index * 2;
    Ok(u16::from_le_bytes([bytes[i], bytes[i + 1]]))
```

### Por que funciona?

LE igual ao C.

### Verifique

site(...,1)==4.

### Código completo alinhado ao solutions/ (RS-RELOC-02)

```rust
PEDAGOGY-SOLUTION: RS-RELOC-02
    let n = reloc_table_len(bytes)?;
    if index >= n { return Err("oob"); }
    let i = index * 2;
    Ok(u16::from_le_bytes([bytes[i], bytes[i + 1]]))
}
pub fn reloc_sites_in_bounds(bytes: &[u8], code_len: usize) -> Result<(), &'static str> {
    // 
```

## RS-RELOC-03

### Onde colocar (RS-RELOC-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função | `reloc_sites_in_bounds` |
| Substituir | o corpo sob o comentário `TODO [RS-RELOC-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Site 7 em code_len 8 deve Err.

### Algoritmo / trace

Para cada site, site+2<=code_len.

### Escreva o código

```rust
    let n = reloc_table_len(bytes)?;
    for i in 0..n {
        let site = reloc_site(bytes, i)? as usize;
        if site + 2 > code_len { return Err("site"); }
    }
    Ok(())
```

### Por que funciona?

Garante espaço para u16 patch.

### Verifique

Ok em site 2; Err em 7.

### Código completo alinhado ao solutions/ (RS-RELOC-03)

```rust
PEDAGOGY-SOLUTION: RS-RELOC-03
    let n = reloc_table_len(bytes)?;
    for i in 0..n {
        let site = reloc_site(bytes, i)? as usize;
        if site + 2 > code_len { return Err("site"); }
    }
    Ok(())
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| BE | use from_le_bytes |

## Relatório de resolução

- TODOs: [ ]
