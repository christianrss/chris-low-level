from tiled_attention_online_softmax import online_softmax_update, finalize
import math

def test_online():
    # PEDAGOGY-TEST: D8-ATT-TILE
    # PEDAGOGY-TEST: D8-ATT-ONLINE
    m, l = online_softmax_update(None, 0.0, [1.0, 2.0, 3.0])
    assert abs(m - 3.0) < 1e-9
    assert abs(l - (math.exp(-2)+math.exp(-1)+1.0)) < 1e-9

def test_out():
    # PEDAGOGY-TEST: D8-ATT-OUT
    assert abs(finalize(0.0, 2.0, 4.0) - 2.0) < 1e-9
