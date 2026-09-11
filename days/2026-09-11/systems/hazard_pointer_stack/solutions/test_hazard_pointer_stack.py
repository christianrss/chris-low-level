from hazard_pointer_stack import HPStack
def test_hp():
    # PEDAGOGY-TEST: D9-HP-PROTECT
    # PEDAGOGY-TEST: D9-HP-PUSH
    # PEDAGOGY-TEST: D9-HP-POP
    s = HPStack(); s.push(1); s.push(2)
    assert s.pop() == 2 and s.pop() == 1 and s.pop() is None
