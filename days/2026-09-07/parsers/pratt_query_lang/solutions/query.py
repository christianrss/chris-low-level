def lex(s):
    # PEDAGOGY-SOLUTION: D5-PRATT-LEX
    out=[];i=0
    while i<len(s):
        if s[i].isspace():i+=1;continue
        if s[i] in "():":out.append(({"(":"LP",")":"RP",":":"COL"}[s[i]],s[i]));i+=1;continue
        if s[i]=='"':
            j=i+1
            while j<len(s) and s[j]!='"': j+=1
            if j==len(s):raise ValueError("unterminated string")
            out.append(("VAL",s[i+1:j]));i=j+1;continue
        j=i
        while j<len(s) and not s[j].isspace() and s[j] not in "():":j+=1
        v=s[i:j];u=v.upper();out.append((u if u in ("AND","OR","NOT") else "WORD",v));i=j
    out.append(("EOF",""));return out
def parse(s):
    toks=lex(s);pos=0
    def peek():return toks[pos]
    def take():
        nonlocal pos;t=toks[pos];pos+=1;return t
    # PEDAGOGY-SOLUTION: D5-PRATT-PARSE
    def expr(minbp=0):
        nonlocal pos
        typ,val=take()
        if typ=="NOT": left=("not",expr(30))
        elif typ=="LP":
            left=expr(0)
            if take()[0]!="RP":raise ValueError("missing )")
        elif typ=="WORD":
            # PEDAGOGY-SOLUTION: D5-PRATT-FIELD
            if peek()[0]=="COL":
                take();t,v=take()
                if t not in ("WORD","VAL"):raise ValueError("field value")
                left=("field",val,v)
            else:left=("text",val)
        elif typ=="VAL":left=("text",val)
        else:raise ValueError("expected expression")
        while True:
            op=peek()[0]
            if op not in ("AND","OR"):break
            lbp,rbp=(20,21) if op=="AND" else (10,11)
            if lbp<minbp:break
            take();right=expr(rbp);left=(op.lower(),left,right)
        return left
    tree=expr()
    if peek()[0]!="EOF":raise ValueError("trailing input")
    return tree
