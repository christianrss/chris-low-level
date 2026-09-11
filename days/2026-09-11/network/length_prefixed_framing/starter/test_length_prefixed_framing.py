from length_prefixed_framing import Framer
def test_frame():
    # PEDAGOGY-TEST: D9-NET-ENCODE
    # PEDAGOGY-TEST: D9-NET-FEED
    # PEDAGOGY-TEST: D9-NET-DECODE
    f = Framer()
    blob = f.encode(b"hi")
    assert blob[:4] == bytes([2,0,0,0])
    f.feed(blob[:3]); assert f.decode_one() is None
    f.feed(blob[3:]); assert f.decode_one() == b"hi"
