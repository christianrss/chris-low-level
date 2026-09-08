import math
def online_softmax(values):
    if not values: raise ValueError("empty")
    # TODO [D6-SM-STATS]: mantenha máximo e denominador online.
    m=0.0; d=1.0
    # TODO [D6-SM-NORMALIZE]: normalize com estatísticas finais.
    return [0.0 for _ in values]
def softmax_two_pass(values):
    # TODO [D6-SM-REFERENCE]: referência estável em duas passagens.
    return [0.0 for _ in values]
