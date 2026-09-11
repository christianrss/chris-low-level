from pike_regex_vm import run

def test_match():
    # PEDAGOGY-TEST: D9-PIKE-EPSILON
    # PEDAGOGY-TEST: D9-PIKE-STEP
    # PEDAGOGY-TEST: D9-PIKE-MATCH
    code = [("CHAR", "a", 1), ("MATCH",)]
    assert run(code, "a") is True
    assert run(code, "b") is False

def test_trace():
    # PEDAGOGY-TEST: D9-PIKE-TRACE
    code = [("CHAR", "a", 1), ("MATCH",)]
    ok, snap = run(code, "a", trace=True)
    assert ok and len(snap) >= 1
