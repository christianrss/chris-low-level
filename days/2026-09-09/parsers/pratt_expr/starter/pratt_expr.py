import re

def lex(src):
    # TODO [D7-PRATT-LEX]
    raise NotImplementedError("D7-PRATT-LEX")

def parse(src):
    toks = lex(src)
    pos = 0
    def expr(min_bp=0):
        nonlocal pos
        # TODO [D7-PRATT-NUD]
        # TODO [D7-PRATT-LED]
        raise NotImplementedError("D7-PRATT-NUD")
    return expr()
