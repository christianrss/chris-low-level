from backtracking_regex_vm import match

def test_char_match():
    # PEDAGOGY-TEST: D8-RE-CHAR
    # PEDAGOGY-TEST: D8-RE-MATCH
    assert match([("CHAR", "a"), ("MATCH",)], "a")
    assert not match([("CHAR", "a"), ("MATCH",)], "b")

def test_star():
    # PEDAGOGY-TEST: D8-RE-STAR
    assert match([("STAR", "a"), ("CHAR", "b"), ("MATCH",)], "aaab")
