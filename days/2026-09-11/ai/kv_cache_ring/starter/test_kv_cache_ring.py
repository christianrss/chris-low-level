from kv_cache_ring import KVRing
def test_kv():
    # PEDAGOGY-TEST: D9-KV-WRITE
    # PEDAGOGY-TEST: D9-KV-READ
    # PEDAGOGY-TEST: D9-KV-WINDOW
    r = KVRing(3)
    r.write("a"); r.write("b"); r.write("c"); r.write("d")
    assert r.window() == ["b", "c", "d"]
    assert r.read(0) == "b"
