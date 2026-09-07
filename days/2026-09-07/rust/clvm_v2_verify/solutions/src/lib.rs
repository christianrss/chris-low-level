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

// PEDAGOGY-SOLUTION: CLVM-RS-V2-HEADER-01
/// Parse header v2: magic, version byte, flags, code_size, checksum; valida FNV sobre body.
pub fn parse_image(data: &[u8]) -> Result<ClvmV2Image, ClvmV2Error> {
    if data.len() < HEADER_SIZE {
        return Err(ClvmV2Error::Truncated);
    }
    if data[0..4] != *MAGIC {
        return Err(ClvmV2Error::BadMagic);
    }
    if data[4] != VERSION {
        return Err(ClvmV2Error::BadVersion);
    }
    let code_size = u32::from_le_bytes([data[8], data[9], data[10], data[11]]) as usize;
    let checksum = u32::from_le_bytes([data[12], data[13], data[14], data[15]]);
    let body = &data[HEADER_SIZE..];
    if fnv1a32(body) != checksum {
        return Err(ClvmV2Error::ChecksumMismatch);
    }
    if body.len() < code_size {
        return Err(ClvmV2Error::Truncated);
    }
    let code = body[..code_size].to_vec();
    let (strings, _) = decode_pool(body, code_size)?;
    Ok(ClvmV2Image { code, strings })
}

// PEDAGOGY-SOLUTION: CLVM-RS-V2-POOL-02
/// Codifica pool: `u32 count` + repetição `(u32 len, utf8 bytes)`.
pub fn encode_pool(strings: &[&str]) -> Vec<u8> {
    let mut out = Vec::new();
    out.extend_from_slice(&(strings.len() as u32).to_le_bytes());
    for s in strings {
        let raw = s.as_bytes();
        out.extend_from_slice(&(raw.len() as u32).to_le_bytes());
        out.extend_from_slice(raw);
    }
    out
}

// PEDAGOGY-SOLUTION: CLVM-RS-V2-POOL-02
/// Decodifica pool a partir de `offset` no buffer (após o segmento `code`).
pub fn decode_pool(data: &[u8], offset: usize) -> Result<(Vec<String>, usize), ClvmV2Error> {
    if offset + 4 > data.len() {
        return Err(ClvmV2Error::Truncated);
    }
    let count = u32::from_le_bytes([
        data[offset],
        data[offset + 1],
        data[offset + 2],
        data[offset + 3],
    ]) as usize;
    let mut pos = offset + 4;
    let mut strings = Vec::with_capacity(count);
    for _ in 0..count {
        if pos + 4 > data.len() {
            return Err(ClvmV2Error::Truncated);
        }
        let n = u32::from_le_bytes([data[pos], data[pos + 1], data[pos + 2], data[pos + 3]])
            as usize;
        pos += 4;
        if pos + n > data.len() {
            return Err(ClvmV2Error::Truncated);
        }
        let raw = &data[pos..pos + n];
        pos += n;
        let s = std::str::from_utf8(raw)
            .map(|v| v.to_string())
            .map_err(|_| ClvmV2Error::Truncated)?;
        strings.push(s);
    }
    Ok((strings, pos))
}

// PEDAGOGY-SOLUTION: CLVM-RS-V2-PRINTS-03
/// Monta imagem mínima: `PRINTS 0` + `HALT`, pool `["hi"]`.
pub fn assemble_hello() -> Vec<u8> {
    let mut code = Vec::with_capacity(4);
    code.push(PRINTS);
    code.extend_from_slice(&0u16.to_le_bytes());
    code.push(HALT);
    build_image(&code, &["hi"])
}

// PEDAGOGY-SOLUTION: CLVM-RS-V2-PRINTS-03
/// Executa subset mini: apenas `PRINTS` e `HALT`; concatena strings com newline.
pub fn run_prints(data: &[u8]) -> Result<String, ClvmV2Error> {
    let image = parse_image(data)?;
    let mut out = Vec::new();
    let mut pc = 0usize;
    while pc < image.code.len() {
        let op = image.code[pc];
        pc += 1;
        match op {
            PRINTS => {
                if pc + 2 > image.code.len() {
                    return Err(ClvmV2Error::TruncatedOperand);
                }
                let idx = u16::from_le_bytes([image.code[pc], image.code[pc + 1]]) as usize;
                pc += 2;
                if idx >= image.strings.len() {
                    return Err(ClvmV2Error::PoolOob);
                }
                out.push(image.strings[idx].clone());
            }
            HALT => break,
            other => return Err(ClvmV2Error::UnsupportedOpcode(other)),
        }
    }
    if out.is_empty() {
        Ok(String::new())
    } else {
        Ok(out.join("\n") + "\n")
    }
}

// PEDAGOGY-SOLUTION: CLVM-RS-V2-STACK-04
/// Walk estático do bytecode v2: operandos, índices de pool e efeitos de pilha (0,0).
/// Retorna lista de mensagens de erro (vazia = OK).
pub fn verify_stack(code: &[u8], pool_len: usize) -> Vec<String> {
    let mut errors = Vec::new();
    let depth = 0i32;
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
                // stack effect (0, 0)
            }
            other => {
                errors.push(format!("unknown opcode 0x{other:02x} at {start}"));
                break;
            }
        }
        if depth < 0 {
            errors.push(format!("stack underflow at {start}"));
            break;
        }
    }
    errors
}

/// Monta header + payload (code || pool) com checksum FNV.
pub fn build_image(code: &[u8], strings: &[&str]) -> Vec<u8> {
    let pool = encode_pool(strings);
    let payload: Vec<u8> = [code, &pool].concat();
    let checksum = fnv1a32(&payload);
    let mut out = Vec::with_capacity(HEADER_SIZE + payload.len());
    out.extend_from_slice(MAGIC);
    out.push(VERSION);
    out.push(0);
    out.extend_from_slice(&0u16.to_le_bytes());
    out.extend_from_slice(&(code.len() as u32).to_le_bytes());
    out.extend_from_slice(&checksum.to_le_bytes());
    out.extend_from_slice(&payload);
    out
}
