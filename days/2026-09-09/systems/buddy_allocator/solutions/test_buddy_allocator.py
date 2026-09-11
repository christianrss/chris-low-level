from buddy_allocator import Buddy

def test_init():
    # PEDAGOGY-TEST: D7-BUDDY-INIT
    b = Buddy(8)
    assert b.size == 8 and b.free[8] == [0]

def test_alloc():
    # PEDAGOGY-TEST: D7-BUDDY-ALLOC
    b = Buddy(8)
    assert b.alloc(3) == 0
    assert b.used[0] == 4
    assert b.alloc(4) == 4

def test_free_merge():
    # PEDAGOGY-TEST: D7-BUDDY-FREE
    b = Buddy(8)
    a = b.alloc(4)
    c = b.alloc(4)
    b.free(a)
    b.free(c)
    assert b.free.get(8) == [0]
