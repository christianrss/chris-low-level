import re
def lex(src):
    # PEDAGOGY-SOLUTION: D7-PRATT-LEX
    out=[];i=0
    while i<len(src):
        if src[i].isspace():i+=1;continue
        m=re.match(r"(?:\d+(?:\.\d*)?|\.\d+)",src[i:])
        if m:out.append(("NUM",float(m.group())));i+=len(m.group());continue
        if src[i] in "+-*/^()":out.append((src[i],src[i]));i+=1;continue
        raise ValueError(f"bad char at {i}")
    out.append(("EOF",None));return out
def parse(src):
    toks=lex(src);pos=0
    def expr(min_bp=0):
        nonlocal pos
        # PEDAGOGY-SOLUTION: D7-PRATT-NUD
        typ,val=toks[pos];pos+=1
        if typ=="NUM":left=("num",val)
        elif typ=="-":left=("neg",expr(40))
        elif typ=="(":
            left=expr(0)
            if toks[pos][0]!=")":raise ValueError("missing )")
            pos+=1
        else:raise ValueError("expected expression")
        # PEDAGOGY-SOLUTION: D7-PRATT-LED
        bp={"+":10,"-":10,"*":20,"/":20,"^":30}
        while toks[pos][0] in bp:
            op=toks[pos][0];lbp=bp[op]
            if lbp<min_bp:break
            pos+=1;rbp=lbp if op=="^" else lbp+1;right=expr(rbp);left=("bin",op,left,right)
        return left
    ast=expr()
    if toks[pos][0]!="EOF":raise ValueError("trailing")
    return ast
