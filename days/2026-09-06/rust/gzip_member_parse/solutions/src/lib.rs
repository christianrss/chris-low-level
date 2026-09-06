//! Parser estrutural de um *member* gzip (RFC 1952) — sem inflate.
//! Valida magic/method/flags, localiza fim do header e lê trailer CRC32/ISIZE.

pub const GZIP_MAGIC: [u8; 2] = [0x1f, 0x8b];
pub const CM_DEFLATE: u8 = 8;

pub const FLG_FTEXT: u8 = 0x01;
pub const FLG_FHCRC: u8 = 0x02;
pub const FLG_FEXTRA: u8 = 0x04;
pub const FLG_FNAME: u8 = 0x08;
pub const FLG_FCOMMENT: u8 = 0x10;
pub const FLG_RESERVED: u8 = 0xE0;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GzipError {
    Truncated,
    BadMagic,
    BadMethod,
    ReservedFlags,
    BadHeader,
    BadTrailer,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GzipMemberView {
    /// Índice do primeiro byte do stream DEFLATE (após header).
    pub deflate_start: usize,
    /// Índice do primeiro byte do trailer (CRC32); deflate está em [start, trailer).
    pub trailer_start: usize,
    pub crc32: u32,
    pub isize: u32,
    pub flags: u8,
}

// PEDAGOGY-SOLUTION: RS-GZ-01
/// Valida magic `1f8b`, method=8 e rejeita flags reservadas.
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

fn skip_cstring(data: &[u8], mut p: usize) -> Result<usize, GzipError> {
    while p < data.len() {
        if data[p] == 0 {
            return Ok(p + 1);
        }
        p += 1;
    }
    Err(GzipError::Truncated)
}

// PEDAGOGY-SOLUTION: RS-GZ-02
/// Localiza o offset onde começa o DEFLATE (após FEXTRA/FNAME/FCOMMENT/FHCRC).
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
    if p > data.len() {
        return Err(GzipError::BadHeader);
    }
    Ok(p)
}

// PEDAGOGY-SOLUTION: RS-GZ-03
/// Lê CRC32 + ISIZE no trailer e monta `GzipMemberView` (member único até EOF).
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

/// CRC32 ISO-HDLC / gzip (poly 0xEDB88320), implementação local sem crates.
pub fn crc32_gzip(data: &[u8]) -> u32 {
    let mut crc = 0xFFFF_FFFFu32;
    for &b in data {
        crc ^= u32::from(b);
        for _ in 0..8 {
            let mask = (crc & 1).wrapping_neg();
            crc = (crc >> 1) ^ (0xEDB8_8320 & mask);
        }
    }
    !crc
}

/// Monta um member gzip mínimo (header fixo 10 bytes + deflate raw + trailer).
/// `deflate_raw` aqui é tratado como opaco (lab não infla).
pub fn build_minimal_member(deflate_raw: &[u8], original: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(10 + deflate_raw.len() + 8);
    out.extend_from_slice(&GZIP_MAGIC);
    out.push(CM_DEFLATE);
    out.push(0); // flags
    out.extend_from_slice(&0u32.to_le_bytes()); // mtime
    out.push(0); // xfl
    out.push(255); // os unknown
    out.extend_from_slice(deflate_raw);
    out.extend_from_slice(&crc32_gzip(original).to_le_bytes());
    out.extend_from_slice(&(original.len() as u32).to_le_bytes());
    out
}
