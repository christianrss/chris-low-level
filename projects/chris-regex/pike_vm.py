def add_thread(code,pc,out,seen):
    # PEDAGOGY-SOLUTION: D9-PIKE-EPSILON
    if pc in seen:return
    seen.add(pc);op=code[pc]
    if op[0]=="JMP":add_thread(code,op[1],out,seen);return
    if op[0]=="SPLIT":add_thread(code,op[1],out,seen);add_thread(code,op[2],out,seen);return
    out.append(pc)
def run(code,text,trace=False):
    # PEDAGOGY-SOLUTION: D9-PIKE-STEP
    cur=[];add_thread(code,0,cur,set());snap=[]
    for ch in text:
        if trace:snap.append(tuple(cur))
        nxt=[];seen=set()
        for pc in cur:
            op=code[pc]
            if op[0]=="CHAR" and ch==op[1]:add_thread(code,op[2],nxt,seen)
            elif op[0]=="ANY":add_thread(code,op[1],nxt,seen)
        cur=nxt
    # PEDAGOGY-SOLUTION: D9-PIKE-TRACE
    if trace:snap.append(tuple(cur))
    # PEDAGOGY-SOLUTION: D9-PIKE-MATCH
    ok=any(code[pc][0]=="MATCH" for pc in cur)
    return (ok,snap) if trace else ok
