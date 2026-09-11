from statevector_bitmask import SV
def test_sv():
    # PEDAGOGY-TEST: D9-Q-SET
    # PEDAGOGY-TEST: D9-Q-GET
    # PEDAGOGY-TEST: D9-Q-NORM
    s = SV(1); s.set(0, 3); s.set(1, 4); s.normalize()
    assert abs(s.get(0) - 0.6) < 1e-9 and abs(s.get(1) - 0.8) < 1e-9
