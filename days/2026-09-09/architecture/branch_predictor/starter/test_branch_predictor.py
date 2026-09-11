from branch_predictor import TwoBit

def test_init_pred():
    # PEDAGOGY-TEST: D7-BR-INIT
    # PEDAGOGY-TEST: D7-BR-PRED
    p = TwoBit()
    assert p.state == 1
    assert p.predict() is False

def test_update():
    # PEDAGOGY-TEST: D7-BR-UPDATE
    p = TwoBit()
    p.update(True); p.update(True)
    assert p.predict() is True
    p.update(False); p.update(False); p.update(False)
    assert p.predict() is False
