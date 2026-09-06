# RESOLUÇÃO GUIADA — Rust / CHRLE byte codec

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `RS-RLE-01` | `starter/src/lib.rs` | `encode` |
| `RS-RLE-02` | `starter/src/lib.rs` | `decode` |
| `RS-RLE-03` | `starter/src/lib.rs` | `round_trip_ok` |

Cada ID existe como `TODO [ID]` no starter e `PEDAGOGY-SOLUTION` / `PEDAGOGY-TEST` no gabarito/testes.

> Trabalhe em `days/2026-09-06/rust/rle_byte_codec/starter/`. `solutions/` só depois.

---

## RS-RLE-01 — encode

### 1. O problema (starter stub)

```rust
pub fn encode(input: &[u8]) -> Vec<u8> {
    let _ = input;
    unimplemented!("RS-RLE-01")
}
```

Sem encode, nenhum teste de layout passa.

### 2. O algoritmo

```text
out ← Vec
extend magic CHRLE
extend le32(input.len())
i ← 0
enquanto i < len: agrupa run ≤255; push count,value; i ← fim do run
```

### 3. Código completo

```rust
pub fn encode(input: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(9 + input.len() * 2);
    out.extend_from_slice(CHRLE_MAGIC);
    let len = input.len() as u32;
    out.extend_from_slice(&len.to_le_bytes());
    let mut i = 0usize;
    while i < input.len() {
        let mut j = i + 1;
        while j < input.len() && input[j] == input[i] && (j - i) < 255 {
            j += 1;
        }
        out.push((j - i) as u8);
        out.push(input[i]);
        i = j;
    }
    out
}
```

### 4. Por que funciona?

- `extend_from_slice(CHRLE_MAGIC)`: 5 bytes ASCII sem NUL.
- `to_le_bytes()`: portável; evita endian bugs em CI.
- `(j - i) < 255`: garante `as u8` seguro; run cheio reinicia no próximo loop.
- Capacity hint: reduz reallocs, não muda o formato.

### 5. Verificação parcial / debug

```powershell
cargo test caso_1_encode_ten_zeros -- --nocapture
```

Esperado: PASS. Se magic falhar, confira `CHRLE_MAGIC` vs `b"CHRLE"`.

---

## RS-RLE-02 — decode

### 1. O problema

```rust
pub fn decode(input: &[u8]) -> Result<Vec<u8>, RleError> {
    let _ = input;
    Err(RleError::Truncated)
}
```

### 2. O algoritmo

Guards → magic → `len` → loop de pares → `LengthMismatch` se tamanho diverge.

### 3. Código completo

```rust
pub fn decode(input: &[u8]) -> Result<Vec<u8>, RleError> {
    if input.len() < 9 {
        return Err(RleError::Truncated);
    }
    if &input[0..5] != CHRLE_MAGIC.as_slice() {
        return Err(RleError::BadMagic);
    }
    let len = u32::from_le_bytes([input[5], input[6], input[7], input[8]]) as usize;
    let mut out = Vec::with_capacity(len);
    let mut p = 9usize;
    while p + 1 < input.len() && out.len() < len {
        let count = input[p];
        let value = input[p + 1];
        p += 2;
        for _ in 0..count {
            if out.len() >= len {
                break;
            }
            out.push(value);
        }
    }
    if out.len() != len {
        return Err(RleError::LengthMismatch);
    }
    Ok(out)
}
```

### 4. Por que funciona?

- `len() < 9` primeiro: evita panic em `input[8]`.
- `p + 1 < input.len()`: par completo antes de ler `value`.
- Parar em `out.len() >= len`: não estoura se count mentir.
- `LengthMismatch`: contrato igual ao C++ `out.size() == len`.

### 5. Debug

Falhou `BadMagic`? Dump `&enc[0..5]`. Falhou `LengthMismatch`? Conte runs vs header.

---

## RS-RLE-03 — round_trip_ok

### 1. O problema

```rust
pub fn round_trip_ok(input: &[u8]) -> bool {
    let _ = input;
    false
}
```

### 2–3. Código

```rust
pub fn round_trip_ok(input: &[u8]) -> bool {
    let encoded = encode(input);
    match decode(&encoded) {
        Ok(decoded) => decoded == input,
        Err(_) => false,
    }
}
```

### 4. Por que funciona?

Compõe 01+02; se um estiver errado, o assert de `caso_3` falha. Não engole `Err` como sucesso.

### 5. Esperado

`cargo test` no starter: todos PASS após os três TODOs.

---

## Relatório de resolução

| ID | Status | Nota |
|----|--------|------|
| RS-RLE-01 | feito | header + runs |
| RS-RLE-02 | feito | Result + bounds |
| RS-RLE-03 | feito | composição |

Comparar com `solutions/src/lib.rs` só após `cargo test` verde no starter.
