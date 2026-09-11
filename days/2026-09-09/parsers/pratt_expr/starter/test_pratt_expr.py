from pratt_expr import lex, parse

def test_lex():
    # PEDAGOGY-TEST: D7-PRATT-LEX
    assert lex("1+2")[:3] == [("NUM", 1.0), ("+", "+"), ("NUM", 2.0)]

def test_nud_led():
    # PEDAGOGY-TEST: D7-PRATT-NUD
    # PEDAGOGY-TEST: D7-PRATT-LED
    ast = parse("2^3^2")
    assert ast[0] == "bin" and ast[1] == "^"
