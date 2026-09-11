from aba_tagged_freelist import TaggedFreelist

def test_tag():
    # PEDAGOGY-TEST: D8-ABA-TAG
    f = TaggedFreelist(4)
    assert f.pack(3, 1) == (3 | (1 << 16))

def test_push_pop():
    # PEDAGOGY-TEST: D8-ABA-PUSH
    # PEDAGOGY-TEST: D8-ABA-POP
    f = TaggedFreelist(3)
    a = f.pop(); b = f.pop()
    f.push(a)
    assert f.pop() == a
