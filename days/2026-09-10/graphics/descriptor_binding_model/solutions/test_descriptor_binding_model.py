from descriptor_binding_model import layout_of, bind, validate_set

def test_desc():
    # PEDAGOGY-TEST: D8-GFX-LAYOUT
    # PEDAGOGY-TEST: D8-GFX-BIND
    # PEDAGOGY-TEST: D8-GFX-SET
    lay = layout_of(0, 1)
    e = bind(lay, 0, 0, "tex")
    assert e["resource"] == "tex"
    assert validate_set(lay, 0, {0: "a", 1: "b"}) is True
