import math

def online_softmax_update(m, l, tile):
    # PEDAGOGY-SOLUTION: D8-ATT-TILE
    # PEDAGOGY-SOLUTION: D8-ATT-ONLINE
    if not tile:
        return m, l
    tm = max(tile)
    nm = tm if m is None else max(m, tm)
    nl = 0.0
    if m is not None:
        nl = l * math.exp(m - nm)
    for x in tile:
        nl += math.exp(x - nm)
    return nm, nl

def finalize(m, l, weighted_sum):
    # PEDAGOGY-SOLUTION: D8-ATT-OUT
    if l == 0:
        return 0.0
    return weighted_sum / l
