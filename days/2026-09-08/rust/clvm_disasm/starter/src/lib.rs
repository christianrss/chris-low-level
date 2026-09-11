//! CLVM bytecode disassembler — Rust port.

pub const PUSH: u8 = 0x01;

pub fn opcode_name(op: u8) -> Option<&'static str> {
    // TODO [CLVM-RS-DIS-01]
    match op {
        _ => None,
    }
}

pub fn instruction_size(op: u8) -> usize {
    // TODO [CLVM-RS-DIS-02]
    let _ = op;
    0
}

pub fn disassemble(code: &[u8]) -> Result<Vec<String>, String> {
    // TODO [CLVM-RS-DIS-03]
    let _ = code;
    Err("CLVM-RS-DIS-03".into())
}
