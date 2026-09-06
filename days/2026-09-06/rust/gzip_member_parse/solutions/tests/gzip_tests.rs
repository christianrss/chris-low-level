use gzip_member_parse::{
    build_minimal_member, deflate_payload_start, parse_member, validate_fixed_header, GzipError,
    FLG_FNAME, FLG_RESERVED, GZIP_MAGIC,
};

// PEDAGOGY-TEST: RS-GZ-01
// Caso 1 — fixed header magic/method/flags
#[test]
fn caso_1_validate_fixed_header() {
    let original = b"hello-gzip";
    let member = build_minimal_member(b"RAWDEFLATE", original);
    let flags = validate_fixed_header(&member).expect("header");
    assert_eq!(flags, 0);
    assert_eq!(&member[0..2], &GZIP_MAGIC);

    let mut bad = member.clone();
    bad[0] = 0x00;
    assert_eq!(validate_fixed_header(&bad), Err(GzipError::BadMagic));

    let mut reserved = member.clone();
    reserved[3] |= FLG_RESERVED;
    assert_eq!(validate_fixed_header(&reserved), Err(GzipError::ReservedFlags));

    assert_eq!(validate_fixed_header(&member[0..5]), Err(GzipError::Truncated));
}

// PEDAGOGY-TEST: RS-GZ-02
// Caso 2 — skip FNAME zero-terminated
#[test]
fn caso_2_deflate_start_with_fname() {
    // 10-byte fixed + "file.txt\0" + opaque deflate + trailer
    let mut data = Vec::new();
    data.extend_from_slice(&GZIP_MAGIC);
    data.push(8);
    data.push(FLG_FNAME);
    data.extend_from_slice(&0u32.to_le_bytes());
    data.push(0);
    data.push(255);
    data.extend_from_slice(b"file.txt\0");
    let deflate_at = data.len();
    data.extend_from_slice(b"XX");
    data.extend_from_slice(&0u32.to_le_bytes());
    data.extend_from_slice(&2u32.to_le_bytes());
    assert_eq!(deflate_payload_start(&data).unwrap(), deflate_at);
}

// PEDAGOGY-TEST: RS-GZ-03
// Caso 3 — parse_member offsets + isize
#[test]
fn caso_3_parse_member_trailer() {
    let original = b"PORTAL";
    let deflate = b"OPAQUE";
    let member = build_minimal_member(deflate, original);
    let view = parse_member(&member).expect("member");
    assert_eq!(view.deflate_start, 10);
    assert_eq!(view.trailer_start, member.len() - 8);
    assert_eq!(&member[view.deflate_start..view.trailer_start], deflate);
    assert_eq!(view.isize, original.len() as u32);
    assert_eq!(view.crc32, gzip_member_parse::crc32_gzip(original));
}
