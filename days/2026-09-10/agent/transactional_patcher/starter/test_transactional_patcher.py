from transactional_patcher import Patcher

def test_tx():
    # PEDAGOGY-TEST: D8-PATCH-BEGIN
    # PEDAGOGY-TEST: D8-PATCH-APPLY
    # PEDAGOGY-TEST: D8-PATCH-COMMIT
    p = Patcher("abcdef")
    p.begin()
    p.apply(2, 4, "ZZ")
    assert p.text == "abZZef"
    p.commit()
    assert p.snap is None
