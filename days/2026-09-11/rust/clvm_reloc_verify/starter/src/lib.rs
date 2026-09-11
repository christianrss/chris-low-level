//! Verify CLVM reloc table bounds.
pub fn reloc_table_len(bytes: &[u8]) -> Result<usize, &'static str> {
    // TODO [RS-RELOC-01]: bytes must be multiple of 2; Ok(n_entries)
    let _ = bytes;
    Err("RS-RELOC-01")
}
pub fn reloc_site(bytes: &[u8], index: usize) -> Result<u16, &'static str> {
    // TODO [RS-RELOC-02]: read u16 LE entry
    let _ = (bytes, index);
    Err("RS-RELOC-02")
}
pub fn reloc_sites_in_bounds(bytes: &[u8], code_len: usize) -> Result<(), &'static str> {
    // TODO [RS-RELOC-03]: every site + 2 <= code_len
    let _ = (bytes, code_len);
    Err("RS-RELOC-03")
}
