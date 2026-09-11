from tlb_page_walk import TLB, PAGE

def test_lookup_fill():
    # PEDAGOGY-TEST: D8-TLB-LOOKUP
    # PEDAGOGY-TEST: D8-TLB-FILL
    t = TLB()
    assert t.lookup(0) is None
    t.fill(0, 7)
    assert t.lookup(100) == 7

def test_walk():
    # PEDAGOGY-TEST: D8-TLB-WALK
    t = TLB()
    assert t.walk(PAGE + 3, {1: 9}) == 9
