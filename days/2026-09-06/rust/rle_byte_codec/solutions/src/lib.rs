//! CHRLE — Run-Length Encoding seguro em Rust (ownership + slices).
//! Magic ASCII `CHRLE` + length LE32 + pares `(count u8, value u8)`.

pub const CHRLE_MAGIC: &[u8; 5] = b"CHRLE";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RleError {
    BadMagic,
    Truncated,
    LengthMismatch,
}

// PEDAGOGY-SOLUTION: RS-RLE-01
/// Codifica `input` no formato CHRLE.
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
        let count = (j - i) as u8;
        out.push(count);
        out.push(input[i]);
        i = j;
    }
    out
}

// PEDAGOGY-SOLUTION: RS-RLE-02
/// Decodifica buffer CHRLE com checagens de bounds.
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

// PEDAGOGY-SOLUTION: RS-RLE-03
/// Round-trip + rejeição de payload malformado.
pub fn round_trip_ok(input: &[u8]) -> bool {
    let encoded = encode(input);
    match decode(&encoded) {
        Ok(decoded) => decoded == input,
        Err(_) => false,
    }
}
