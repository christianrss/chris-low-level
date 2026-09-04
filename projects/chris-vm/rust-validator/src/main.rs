// Safe structural validator for CLVM files; it never executes bytecode.
use std::{env, fs};

fn fnv1a32(data: &[u8]) -> u32 {
    let mut h = 0x811c9dc5u32;
    for &b in data { h ^= b as u32; h = h.wrapping_mul(0x01000193); }
    h
}
fn u16le(p: &[u8]) -> u16 { u16::from_le_bytes([p[0],p[1]]) }
fn u32le(p: &[u8]) -> u32 { u32::from_le_bytes([p[0],p[1],p[2],p[3]]) }

fn validate(data: &[u8]) -> Result<(), String> {
    if data.len() < 16 { return Err("file too small".into()); }
    if &data[0..4] != b"CLVM" { return Err("bad magic".into()); }
    if data[4] != 1 { return Err("unsupported version".into()); }
    if data[5] != 0 { return Err("unsupported flags".into()); }
    let entry = u16le(&data[6..8]) as usize;
    let size = u32le(&data[8..12]) as usize;
    let expected = u32le(&data[12..16]);
    if size != data.len()-16 { return Err("size mismatch".into()); }
    if size != 0 && entry >= size { return Err("entry outside code".into()); }
    let code=&data[16..];
    if fnv1a32(code) != expected { return Err("checksum mismatch".into()); }

    let mut pc=0usize;
    while pc < code.len() {
        let op=code[pc]; pc += 1;
        match op {
            0x01 => { if pc+4 > code.len() { return Err("truncated PUSH".into()); } pc += 4; }
            0x09|0x0a => { if pc+2 > code.len() { return Err("truncated branch".into()); } pc += 2; }
            0x02..=0x08 => {}
            _ => return Err(format!("unknown opcode 0x{op:02x}")),
        }
    }
    Ok(())
}
fn main() {
    let path=env::args().nth(1).unwrap_or_else(|| { eprintln!("usage: clvm-validator <file>"); std::process::exit(2) });
    let data=fs::read(&path).unwrap_or_else(|e| { eprintln!("read error: {e}"); std::process::exit(2) });
    match validate(&data) { Ok(()) => println!("VALID: {path}"), Err(e) => { eprintln!("INVALID: {e}"); std::process::exit(1) } }
}
