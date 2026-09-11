from welford_layernorm import welford, layernorm

def test_mean_var():
    # PEDAGOGY-TEST: D7-WEL-MEAN
    # PEDAGOGY-TEST: D7-WEL-VAR
    m, v = welford([1.0, 2.0, 3.0])
    assert abs(m - 2.0) < 1e-9
    assert abs(v - (2.0 / 3.0)) < 1e-9

def test_norm():
    # PEDAGOGY-TEST: D7-WEL-NORM
    y = layernorm([1.0, 2.0, 3.0], eps=0.0)
    assert abs(sum(y)) < 1e-9
