// PEDAGOGY-TEST: CAP-RS-XVFY-01
// PEDAGOGY-TEST: CAP-RS-XVFY-02
// PEDAGOGY-TEST: CAP-RS-XVFY-03
use cross_verify_clvm::{validate_header, extract_code, verify_checksum, fnv1a32};

#[test]
fn caso1_header() {
    let mut img = vec![b'C', b'L', b'V', b'M', 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0x08, 0x08];
    let c = fnv1a32(&img[16..]);
    img[12..16].copy_from_slice(&c.to_le_bytes());
    assert!(validate_header(&img));
    assert_eq!(extract_code(&img), Some(vec![0x08, 0x08]));
    assert!(verify_checksum(&img));
}
