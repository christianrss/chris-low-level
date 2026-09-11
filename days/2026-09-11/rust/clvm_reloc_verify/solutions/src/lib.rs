//! Verify CLVM reloc table bounds.
pub fn reloc_table_len(bytes: &[u8]) -> Result<usize, &'static str> {
    // PEDAGOGY-SOLUTION: RS-RELOC-01
    if bytes.len() % 2 != 0 { return Err("odd"); }
    Ok(bytes.len() / 2)
}
pub fn reloc_site(bytes: &[u8], index: usize) -> Result<u16, &'static str> {
    // PEDAGOGY-SOLUTION: RS-RELOC-02
    let n = reloc_table_len(bytes)?;
    if index >= n { return Err("oob"); }
    let i = index * 2;
    Ok(u16::from_le_bytes([bytes[i], bytes[i + 1]]))
}
pub fn reloc_sites_in_bounds(bytes: &[u8], code_len: usize) -> Result<(), &'static str> {
    // PEDAGOGY-SOLUTION: RS-RELOC-03
    let n = reloc_table_len(bytes)?;
    for i in 0..n {
        let site = reloc_site(bytes, i)? as usize;
        if site + 2 > code_len { return Err("site"); }
    }
    Ok(())
}
