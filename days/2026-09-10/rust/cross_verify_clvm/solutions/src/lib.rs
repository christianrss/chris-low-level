//! Cross-verify CLVM bytecode with Python reference (FNV checksum).

pub const MAGIC: &[u8; 4] = b"CLVM";

pub fn fnv1a32(data: &[u8]) -> u32 {
    let mut h = 0x811C_9DC5u32;
    for &b in data {
        h ^= u32::from(b);
        h = h.wrapping_mul(0x0100_0193);
    }
    h
}

/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-01
pub fn validate_header(data: &[u8]) -> bool {
    data.len() >= 16 && data.starts_with(MAGIC) && data[4] == 1
}

/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-02
pub fn extract_code(data: &[u8]) -> Option<Vec<u8>> {
    if data.len() < 16 { return None; }
    let size = u32::from_le_bytes(data[8..12].try_into().unwrap()) as usize;
    if data.len() < 16 + size { return None; }
    Some(data[16..16+size].to_vec())
}

/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-03
pub fn verify_checksum(data: &[u8]) -> bool {
    let code = match extract_code(data) {
        Some(c) => c,
        None => return false,
    };
    let expected = u32::from_le_bytes(data[12..16].try_into().unwrap());
    fnv1a32(&code) == expected
}
