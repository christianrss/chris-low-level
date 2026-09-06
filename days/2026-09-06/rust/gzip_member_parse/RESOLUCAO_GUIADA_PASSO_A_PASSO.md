# RESOLUÇÃO GUIADA — Rust / Gzip member parse

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `RS-GZ-01` | `starter/src/lib.rs` | `validate_fixed_header` |
| `RS-GZ-02` | `starter/src/lib.rs` | `deflate_payload_start` |
| `RS-GZ-03` | `starter/src/lib.rs` | `parse_member` |

> Trabalhe em `days/2026-09-06/rust/gzip_member_parse/starter/`.  
> `crc32_gzip` e `build_minimal_member` já estão prontos.

---

## RS-GZ-01 — validate_fixed_header

### 1. O problema (starter stub)

```rust
pub fn validate_fixed_header(data: &[u8]) -> Result<u8, GzipError> {
    let _ = data;
    Err(GzipError::Truncated)
}
```

### 2. O algoritmo

```text
len < 10 → Truncated
magic → BadMagic; CM → BadMethod; flags&0xE0 → ReservedFlags
Ok(flags)
```

### 3. Código completo

```rust
pub fn validate_fixed_header(data: &[u8]) -> Result<u8, GzipError> {
    if data.len() < 10 {
        return Err(GzipError::Truncated);
    }
    if data[0] != GZIP_MAGIC[0] || data[1] != GZIP_MAGIC[1] {
        return Err(GzipError::BadMagic);
    }
    if data[2] != CM_DEFLATE {
        return Err(GzipError::BadMethod);
    }
    let flags = data[3];
    if flags & FLG_RESERVED != 0 {
        return Err(GzipError::ReservedFlags);
    }
    Ok(flags)
}
```

### 4. Por que funciona?

- Checa `len` antes de qualquer índice.
- `FLG_RESERVED = 0xE0` captura bits 5–7 de uma vez.
- Retorna `flags` para o próximo TODO reutilizar sem reler.

### 5. Debug / esperado

`cargo test caso_1_validate_fixed_header` → PASS.

---

## RS-GZ-02 — deflate_payload_start

### 1. O problema

```rust
pub fn deflate_payload_start(data: &[u8]) -> Result<usize, GzipError> {
    let _ = data;
    Err(GzipError::Truncated)
}
```

### 2. O algoritmo

Chame `validate_fixed_header`; `p=10`; processe FEXTRA → FNAME → FCOMMENT → FHCRC.

### 3. Código completo

```rust
fn skip_cstring(data: &[u8], mut p: usize) -> Result<usize, GzipError> {
    while p < data.len() {
        if data[p] == 0 {
            return Ok(p + 1);
        }
        p += 1;
    }
    Err(GzipError::Truncated)
}

pub fn deflate_payload_start(data: &[u8]) -> Result<usize, GzipError> {
    let flags = validate_fixed_header(data)?;
    let mut p = 10usize;
    if flags & FLG_FEXTRA != 0 {
        if p + 2 > data.len() {
            return Err(GzipError::Truncated);
        }
        let xlen = u16::from_le_bytes([data[p], data[p + 1]]) as usize;
        p += 2;
        if p + xlen > data.len() {
            return Err(GzipError::Truncated);
        }
        p += xlen;
    }
    if flags & FLG_FNAME != 0 {
        p = skip_cstring(data, p)?;
    }
    if flags & FLG_FCOMMENT != 0 {
        p = skip_cstring(data, p)?;
    }
    if flags & FLG_FHCRC != 0 {
        if p + 2 > data.len() {
            return Err(GzipError::Truncated);
        }
        p += 2;
    }
    Ok(p)
}
```

### 4. Por que funciona?

- Reusa 01 (DRY + mesma política de erro).
- `skip_cstring` inclui o NUL no avanço (`p+1`).
- Cada ramo verifica bounds antes de ler.

### 5. Debug

`caso_2` monta FNAME=`file.txt\0`; se falhar, conte bytes após o fixo (deve ser 9).

---

## RS-GZ-03 — parse_member

### 1. O problema

Stub retorna `Truncated`; testes precisam da view completa.

### 2–3. Código

```rust
pub fn parse_member(data: &[u8]) -> Result<GzipMemberView, GzipError> {
    let flags = validate_fixed_header(data)?;
    let deflate_start = deflate_payload_start(data)?;
    if data.len() < deflate_start + 8 {
        return Err(GzipError::BadTrailer);
    }
    let trailer_start = data.len() - 8;
    if trailer_start < deflate_start {
        return Err(GzipError::BadTrailer);
    }
    let crc32 = u32::from_le_bytes([
        data[trailer_start],
        data[trailer_start + 1],
        data[trailer_start + 2],
        data[trailer_start + 3],
    ]);
    let isize = u32::from_le_bytes([
        data[trailer_start + 4],
        data[trailer_start + 5],
        data[trailer_start + 6],
        data[trailer_start + 7],
    ]);
    Ok(GzipMemberView {
        deflate_start,
        trailer_start,
        crc32,
        isize,
        flags,
    })
}
```

### 4. Por que funciona?

Member único até EOF → trailer = últimos 8 bytes. `build_minimal_member` grava CRC/ISIZE assim; o teste compara com `crc32_gzip(original)`.

### 5. Esperado

`cargo test` no starter: 3 testes PASS.

---

## Relatório de resolução

| ID | Status | Nota |
|----|--------|------|
| RS-GZ-01 | feito | header fixo |
| RS-GZ-02 | feito | opcionais RFC |
| RS-GZ-03 | feito | trailer + view |

Compare com `solutions/src/lib.rs` apenas após verde no starter.
