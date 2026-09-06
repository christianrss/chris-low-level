//! CHRLE — Run-Length Encoding seguro em Rust (ownership + slices).
//! Magic ASCII `CHRLE` + length LE32 + pares `(count u8, value u8)`.

pub const CHRLE_MAGIC: &[u8; 5] = b"CHRLE";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RleError {
    BadMagic,
    Truncated,
    LengthMismatch,
}

/// Codifica `input` no formato CHRLE.
///
/// TODO [RS-RLE-01]
pub fn encode(input: &[u8]) -> Vec<u8> {
    let _ = input;
    unimplemented!("RS-RLE-01")
}

/// Decodifica buffer CHRLE com checagens de bounds.
///
/// TODO [RS-RLE-02]
pub fn decode(input: &[u8]) -> Result<Vec<u8>, RleError> {
    let _ = input;
    Err(RleError::Truncated)
}

/// Round-trip + rejeição de payload malformado.
///
/// TODO [RS-RLE-03]
pub fn round_trip_ok(input: &[u8]) -> bool {
    let _ = input;
    false
}
