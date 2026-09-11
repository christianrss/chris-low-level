use clvm_disasm::{disassemble, instruction_size, opcode_name, PUSH};

// PEDAGOGY-TEST: CLVM-RS-DIS-01
// Caso 1: opcode_name HALT
#[test]
fn caso_1_opcode_name() {
    assert_eq!(opcode_name(PUSH), Some("PUSH"));
    assert_eq!(opcode_name(0x08), Some("HALT"));
}

// PEDAGOGY-TEST: CLVM-RS-DIS-02
// Caso 2: instruction_size PUSH=5
#[test]
fn caso_2_instruction_size() {
    assert_eq!(instruction_size(PUSH), 5);
    assert_eq!(instruction_size(0x09), 3);
    assert_eq!(instruction_size(0x08), 1);
}

// PEDAGOGY-TEST: CLVM-RS-DIS-03
// Caso 3: disassemble PUSH 42 HALT
#[test]
fn caso_3_disassemble_push_halt() {
    let code = [PUSH, 42, 0, 0, 0, 0x08];
    let lines = disassemble(&code).expect("disasm");
    assert_eq!(lines, vec!["PUSH 42", "HALT"]);
}

// PEDAGOGY-TEST: CLVM-RS-DIS-03
// Caso 4: unknown opcode error
#[test]
fn caso_4_unknown_op_err() {
    assert!(disassemble(&[0xFF]).is_err());
}
