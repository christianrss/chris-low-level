from robin_hood_hash import RobinHood
def test_rh():
    # PEDAGOGY-TEST: D9-RH-PROBE
    # PEDAGOGY-TEST: D9-RH-INSERT
    # PEDAGOGY-TEST: D9-RH-LOOKUP
    h = RobinHood(8)
    i = h.insert("a")
    assert h.lookup("a") == i
    assert h.lookup("missing") is None
