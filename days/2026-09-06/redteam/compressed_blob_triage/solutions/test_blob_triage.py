# PEDAGOGY-TEST: RT-COMP-01: magic bytes 1F8B e 789C
# PEDAGOGY-TEST: RT-COMP-02: size limits compressed/uncompressed
# PEDAGOGY-TEST: RT-COMP-03: strings ASCII no payload
import gzip
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from blob_triage import (
    detect_compression_magic,
    extract_ascii_strings,
    validate_size_limits,
)


def test_gzip_magic() -> None:
    payload = gzip.compress(b"hello triage")
    assert detect_compression_magic(payload) == "gzip"


def test_zlib_magic() -> None:
    payload = zlib.compress(b"zlib header test")
    assert payload[:2] == b"\x78\x9c"
    assert detect_compression_magic(payload) == "zlib"


def test_size_limits() -> None:
    big = gzip.compress(b"x" * 200_000)
    assert not validate_size_limits(big, max_compressed=100_000, max_uncompressed=50_000)
    small = gzip.compress(b"ok")
    assert validate_size_limits(small, max_compressed=10_000, max_uncompressed=10_000)


def test_strings_in_payload() -> None:
    raw = b"\x00SECRET_KEY=abc123\xff" + gzip.compress(b"noise")
    strings = extract_ascii_strings(raw, min_len=4)
    assert "SECRET_KEY=abc123" in strings


if __name__ == "__main__":
    test_gzip_magic()
    test_zlib_magic()
    test_size_limits()
    test_strings_in_payload()
    print("OK blob triage")
