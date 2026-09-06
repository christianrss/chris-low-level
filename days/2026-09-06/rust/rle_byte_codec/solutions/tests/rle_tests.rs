use rle_byte_codec::{decode, encode, round_trip_ok, RleError, CHRLE_MAGIC};

// PEDAGOGY-TEST: RS-RLE-01
// Caso 1 — ten zeros round-trip via encode path
#[test]
fn caso_1_encode_ten_zeros() {
    let input = vec![0u8; 10];
    let enc = encode(&input);
    assert!(enc.len() >= 9);
    assert_eq!(&enc[0..5], CHRLE_MAGIC.as_slice());
    let len = u32::from_le_bytes([enc[5], enc[6], enc[7], enc[8]]);
    assert_eq!(len, 10);
    assert_eq!(enc[9], 10);
    assert_eq!(enc[10], 0);
}

// PEDAGOGY-TEST: RS-RLE-02
// Caso 2 — decode ABCD literals
#[test]
fn caso_2_decode_abcd() {
    let input = b"ABCD".to_vec();
    let enc = encode(&input);
    let dec = decode(&enc).expect("decode");
    assert_eq!(dec, input);
}

// PEDAGOGY-TEST: RS-RLE-03
// Caso 3 — round-trip helper + bad magic rejected
#[test]
fn caso_3_round_trip_and_bad_magic() {
    assert!(round_trip_ok(b"AAAAABBBCC"));
    let mut bad = encode(b"hi");
    bad[0] = b'X';
    assert_eq!(decode(&bad), Err(RleError::BadMagic));
    assert_eq!(decode(&bad[0..4]), Err(RleError::Truncated));
}
