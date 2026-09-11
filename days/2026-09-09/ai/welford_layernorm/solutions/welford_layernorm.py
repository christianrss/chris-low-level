import math

def welford(xs):
    # PEDAGOGY-SOLUTION: D7-WEL-MEAN
    # PEDAGOGY-SOLUTION: D7-WEL-VAR
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    var = m2 / n if n else 0.0
    return mean, var

def layernorm(xs, eps=1e-5):
    # PEDAGOGY-SOLUTION: D7-WEL-NORM
    mean, var = welford(xs)
    s = math.sqrt(var + eps)
    return [(x - mean) / s for x in xs]
