import math
def online_softmax(values):
    if not values: raise ValueError("empty")
    # PEDAGOGY-SOLUTION: D6-SM-STATS
    m=float("-inf"); d=0.0
    for x in values:
        m_new=max(m,x); d=d*math.exp(m-m_new)+math.exp(x-m_new); m=m_new
    # PEDAGOGY-SOLUTION: D6-SM-NORMALIZE
    return [math.exp(x-m)/d for x in values]
def softmax_two_pass(values):
    # PEDAGOGY-SOLUTION: D6-SM-REFERENCE
    if not values: raise ValueError("empty")
    m=max(values); ex=[math.exp(x-m) for x in values]; s=sum(ex)
    return [x/s for x in ex]
