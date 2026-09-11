//! CLVM bytecode disassembler — Rust port.

pub const PUSH: u8 = 0x01;

pub fn opcode_name(op: u8) -> Option<&'static str> {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-01
    match op {
        0x02 => Some("ADD"),
        0x08 => Some("HALT"),
        0x09 => Some("JMP"),
        PUSH => Some("PUSH"),
        _ => None,
    }
}

pub fn instruction_size(op: u8) -> usize {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-02
    if op == PUSH {
        5
    } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {
        3
    } else {
        1
    }
}

pub fn disassemble(code: &[u8]) -> Result<Vec<String>, String> {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-03
    let mut out = Vec::new();
    let mut pc = 0usize;
    while pc < code.len() {
        let op = code[pc];
        if op == PUSH {
            if pc + 5 > code.len() {
                return Err("truncated PUSH".into());
            }
            let imm = u32::from_le_bytes(code[pc + 1..pc + 5].try_into().unwrap());
            out.push(format!("PUSH {}", imm));
            pc += 5;
        } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {
            if pc + 3 > code.len() {
                return Err("truncated branch".into());
            }
            let off = u16::from_le_bytes(code[pc + 1..pc + 3].try_into().unwrap());
            let name = opcode_name(op).unwrap_or("BR");
            out.push(format!("{} {}", name, off));
            pc += 3;
        } else if let Some(name) = opcode_name(op) {
            out.push(name.to_string());
            pc += 1;
        } else {
            return Err(format!("unknown op 0x{:02x}", op));
        }
    }
    Ok(out)
}
