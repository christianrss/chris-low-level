use clvm_reloc_verify::*;
#[test]
fn pedagogy_rs_reloc_01() {
    // PEDAGOGY-TEST: RS-RELOC-01
    assert_eq!(reloc_table_len(&[0x02, 0x00]).unwrap(), 1);
    assert!(reloc_table_len(&[0x02]).is_err());
}
#[test]
fn pedagogy_rs_reloc_02() {
    // PEDAGOGY-TEST: RS-RELOC-02
    assert_eq!(reloc_site(&[0x02, 0x00, 0x04, 0x00], 1).unwrap(), 4);
}
#[test]
fn pedagogy_rs_reloc_03() {
    // PEDAGOGY-TEST: RS-RELOC-03
    assert!(reloc_sites_in_bounds(&[0x02, 0x00], 8).is_ok());
    assert!(reloc_sites_in_bounds(&[0x07, 0x00], 8).is_err()); // 7+2>8
}
