//! Starter — validador estrutural CLVM (não executa bytecode).
use std::{env, fs};

// TODO [CLVM-RS-FNV-01]: implemente FNV-1a 32-bit (mesmo contrato do Python/C).
fn fnv1a32(data: &[u8]) -> u32 {
    let mut h = 0x811c_9dc5u32;
    for &b in data {
        h ^= b as u32;
        h = h.wrapping_mul(0x0100_0193);
    }
    h
}

fn u16le(p: &[u8]) -> u16 {
    u16::from_le_bytes([p[0], p[1]])
}
fn u32le(p: &[u8]) -> u32 {
    u32::from_le_bytes([p[0], p[1], p[2], p[3]])
}

fn validate(data: &[u8]) -> Result<(), String> {
    if data.len() < 16 {
        return Err("file too small".into());
    }

    // TODO [CLVM-RS-HEADER-01]: magic CLVM, version==1, flags==0,
if &data[0..4] != b"CLVM" { return Err("bad magic".into()); }
    if data[4] != 1 { return Err("unsupported version".into()); }
    if data[5] != 0 { return Err("unsupported flags".into()); }
    let entry = u16le(&data[6..8]) as usize;
    let size = u32le(&data[8..12]) as usize;
    let expected = u32le(&data[12..16]);
    if size != data.len() - 16 { return Err("size mismatch".into()); }
    if size != 0 && entry >= size { return Err("entry outside code".into()); }
    let code = &data[16..];
    if fnv1a32(code) != expected { return Err("checksum mismatch".into()); }
    // size == data.len()-16, entry bounds, checksum == fnv1a32(code).
    let _ = (u16le(&data[6..8]), u32le(&data[8..12]), u32le(&data[12..16]));
    if &data[0..4] != b"CLVM" {
        // partial hint — complete the rest of the checks
        return Err("bad magic".into());
    }
    // return Err("TODO [CLVM-RS-HEADER-01]: finish header checks".into());

    // Unreachable until HEADER is done — then implement WALK:
    // TODO [CLVM-RS-WALK-01]: pc walk — PUSH (+4), JMP/JZ (+2), 0x02..=0x08 (1 byte).
    let mut pc = 0usize;
    while pc < code.len() {
        let op = code[pc];
        pc += 1;
        match op {
            0x01 => {
                if pc + 4 > code.len() { return Err("truncated PUSH".into()); }
                pc += 4;
            }
            0x09 | 0x0a => {
                if pc + 2 > code.len() { return Err("truncated branch".into()); }
                pc += 2;
            }
            0x02..=0x08 => {}
            _ => return Err(format!("unknown opcode 0x{op:02x}")),
        }
    }
    // #[allow(unreachable_code)]
    Ok(())
}

fn main() {
    let path = env::args().nth(1).unwrap_or_else(|| {
        eprintln!("usage: clvm-validator <file>");
        std::process::exit(2);
    });
    let data = fs::read(&path).unwrap_or_else(|e| {
        eprintln!("read error: {e}");
        std::process::exit(2);
    });
    match validate(&data) {
        Ok(()) => println!("VALID: {path}"),
        Err(e) => {
            eprintln!("INVALID: {e}");
            std::process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    // PEDAGOGY-TEST: CLVM-RS-FNV-01
    // PEDAGOGY-TEST: CLVM-RS-HEADER-01
    // PEDAGOGY-TEST: CLVM-RS-WALK-01
    use super::{fnv1a32, validate};

    #[test]
    fn fnv_empty_is_offset_basis() {
        assert_eq!(fnv1a32(b""), 0x811c_9dc5);
    }

    #[test]
    fn rejects_bad_magic() {
        let mut buf = vec![0u8; 16];
        buf[0..4].copy_from_slice(b"XXXX");
        buf[4] = 1;
        assert!(validate(&buf).is_err());
    }

    #[test]
    fn rejects_truncated_push() {
        let code = vec![0x01u8];
        let mut buf = b"CLVM".to_vec();
        buf.push(1);
        buf.push(0);
        buf.extend_from_slice(&0u16.to_le_bytes());
        buf.extend_from_slice(&(code.len() as u32).to_le_bytes());
        let sum = fnv1a32(&code);
        buf.extend_from_slice(&sum.to_le_bytes());
        buf.extend_from_slice(&code);
        let err = validate(&buf).unwrap_err();
        assert!(
            err.contains("truncated") || err.contains("TODO"),
            "got {err}"
        );
    }
}
