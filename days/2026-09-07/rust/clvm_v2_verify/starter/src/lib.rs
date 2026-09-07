//! CLVM v2 — parser de imagem, pool de strings, opcode PRINTS e verificação estática.
//! Wire format: `days/2026-09-07/systems/clvm_v2_strings/solutions/clvm_v2.py`

pub const MAGIC: &[u8; 4] = b"CLVM";
pub const VERSION: u8 = 2;
pub const HEADER_SIZE: usize = 16;

pub const PRINTS: u8 = 0x21;
pub const HALT: u8 = 0x08;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ClvmV2Error {
    Truncated,
    BadMagic,
    BadVersion,
    ChecksumMismatch,
    PoolOob,
    UnsupportedOpcode(u8),
    TruncatedOperand,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClvmV2Image {
    pub code: Vec<u8>,
    pub strings: Vec<String>,
}

/// FNV-1a 32-bit (mesmo polinômio do loader Python/C++ do curso).
pub fn fnv1a32(data: &[u8]) -> u32 {
    let mut h = 0x811C_9DC5u32;
    for &b in data {
        h ^= u32::from(b);
        h = h.wrapping_mul(0x0100_0193);
    }
    h
}

/// Parse header v2: magic, version byte, flags, code_size, checksum; valida FNV sobre body.
///
/// TODO [CLVM-RS-V2-HEADER-01]
pub fn parse_image(data: &[u8]) -> Result<ClvmV2Image, ClvmV2Error> {
    let _ = data;
    Err(ClvmV2Error::Truncated)
}

/// Codifica pool: `u32 count` + repetição `(u32 len, utf8 bytes)`.
///
/// TODO [CLVM-RS-V2-POOL-02]
pub fn encode_pool(strings: &[&str]) -> Vec<u8> {
    let _ = strings;
    Vec::new()
}

/// Decodifica pool a partir de `offset` no buffer (após o segmento `code`).
///
/// TODO [CLVM-RS-V2-POOL-02]
pub fn decode_pool(data: &[u8], offset: usize) -> Result<(Vec<String>, usize), ClvmV2Error> {
    let _ = (data, offset);
    Err(ClvmV2Error::Truncated)
}

/// Monta imagem mínima: `PRINTS 0` + `HALT`, pool `["hi"]`.
///
/// TODO [CLVM-RS-V2-PRINTS-03]
pub fn assemble_hello() -> Vec<u8> {
    unimplemented!("CLVM-RS-V2-PRINTS-03")
}

/// Executa subset mini: apenas `PRINTS` e `HALT`; concatena strings com newline.
///
/// TODO [CLVM-RS-V2-PRINTS-03]
pub fn run_prints(data: &[u8]) -> Result<String, ClvmV2Error> {
    let _ = data;
    Err(ClvmV2Error::Truncated)
}

/// Walk estático do bytecode v2: operandos, índices de pool e efeitos de pilha (0,0).
/// Retorna lista de mensagens de erro (vazia = OK).
///
/// TODO [CLVM-RS-V2-STACK-04]
pub fn verify_stack(code: &[u8], pool_len: usize) -> Vec<String> {
    let _ = (code, pool_len);
    vec!["stub: CLVM-RS-V2-STACK-04".into()]
}

/// Monta header + payload (code || pool) com checksum FNV.
pub fn build_image(code: &[u8], strings: &[&str]) -> Vec<u8> {
    let pool = encode_pool(strings);
    let payload: Vec<u8> = [code, &pool].concat();
    let checksum = fnv1a32(&payload);
    let mut out = Vec::with_capacity(HEADER_SIZE + payload.len());
    out.extend_from_slice(MAGIC);
    out.push(VERSION);
    out.push(0); // flags
    out.extend_from_slice(&0u16.to_le_bytes()); // reserved
    out.extend_from_slice(&(code.len() as u32).to_le_bytes());
    out.extend_from_slice(&checksum.to_le_bytes());
    out.extend_from_slice(&payload);
    out
}
