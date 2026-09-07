use clvm_v2_verify::{
    assemble_hello, build_image, decode_pool, encode_pool, fnv1a32, parse_image, run_prints,
    verify_stack, ClvmV2Error, HALT, MAGIC, PRINTS, VERSION,
};
use std::fs;
use std::path::PathBuf;

fn fixture(name: &str) -> Vec<u8> {
    let mut p = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    p.push("fixtures");
    p.push(name);
    fs::read(p).expect("fixture")
}

// PEDAGOGY-TEST: CLVM-RS-V2-HEADER-01
#[test]
fn caso_1_parse_header_hello_fixture() {
    let data = fixture("hello_v2.clvm");
    let img = parse_image(&data).expect("parse");
    assert_eq!(img.strings, vec!["hi".to_string()]);
    assert_eq!(img.code[0], PRINTS);
    assert_eq!(img.code[3], HALT);
}

// PEDAGOGY-TEST: CLVM-RS-V2-HEADER-01
#[test]
fn caso_2_reject_bad_magic_and_checksum() {
    assert_eq!(parse_image(&fixture("bad_magic.clvm")), Err(ClvmV2Error::BadMagic));
    assert_eq!(
        parse_image(&fixture("bad_checksum.clvm")),
        Err(ClvmV2Error::ChecksumMismatch)
    );
}

// PEDAGOGY-TEST: CLVM-RS-V2-POOL-02
#[test]
fn caso_3_pool_round_trip() {
    let pool = encode_pool(&["hi", "world"]);
    let (decoded, end) = decode_pool(&pool, 0).expect("decode");
    assert_eq!(decoded, vec!["hi".to_string(), "world".to_string()]);
    assert_eq!(end, pool.len());
}

// PEDAGOGY-TEST: CLVM-RS-V2-PRINTS-03
#[test]
fn caso_4_run_prints_stdout() {
    let img = assemble_hello();
    assert_eq!(run_prints(&img).expect("run"), "hi\n");
    assert_eq!(run_prints(&fixture("hello_v2.clvm")).expect("fixture"), "hi\n");
}

// PEDAGOGY-TEST: CLVM-RS-V2-STACK-04
#[test]
fn caso_5_verify_stack_clean_and_oob() {
    let code = vec![PRINTS, 0x00, 0x00, HALT];
    assert!(verify_stack(&code, 1).is_empty());
    let bad = vec![PRINTS, 0x01, 0x00, HALT];
    let errs = verify_stack(&bad, 1);
    assert!(!errs.is_empty());
    assert!(errs[0].contains("OOB"));
}

// PEDAGOGY-TEST: CLVM-RS-V2-HEADER-01
#[test]
fn caso_6_build_image_checksum_matches_fnv() {
    let code = vec![PRINTS, 0, 0, HALT];
    let img = build_image(&code, &["x"]);
    assert_eq!(&img[0..4], MAGIC);
    assert_eq!(img[4], VERSION);
    let body = &img[16..];
    let stored = u32::from_le_bytes([img[12], img[13], img[14], img[15]]);
    assert_eq!(stored, fnv1a32(body));
}
