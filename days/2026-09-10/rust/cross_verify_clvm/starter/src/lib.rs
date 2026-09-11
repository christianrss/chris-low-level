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

/// TODO [CAP-RS-XVFY-01]: validate magic + version byte == 1
pub fn validate_header(data: &[u8]) -> bool {
    let _ = data;
    false
}

/// TODO [CAP-RS-XVFY-02]: extract code segment after 16-byte header
pub fn extract_code(data: &[u8]) -> Option<Vec<u8>> {
    let _ = data;
    None
}

/// TODO [CAP-RS-XVFY-03]: compare FNV checksum at header offset 12..16
pub fn verify_checksum(data: &[u8]) -> bool {
    let _ = data;
    false
}
