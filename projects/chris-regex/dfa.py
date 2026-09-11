def epsilon_closure(trans,states):
    # PEDAGOGY-SOLUTION: D6-DFA-CLOSURE
    seen=set(states); stack=list(states)
    while stack:
        s=stack.pop()
        for sym,t in trans.get(s,[]):
            if sym is None and t not in seen: seen.add(t); stack.append(t)
    return seen
def subset_construct(trans,start,accept):
    # PEDAGOGY-SOLUTION: D6-DFA-SUBSET
    alphabet=sorted({sym for edges in trans.values() for sym,_ in edges if sym is not None})
    s0=frozenset(epsilon_closure(trans,{start})); ids={s0:0}; q=[s0]; table={}; accepting=set()
    while q:
        cur=q.pop(0); cid=ids[cur]
        if accept in cur: accepting.add(cid)
        for sym in alphabet:
            moved={t for s in cur for a,t in trans.get(s,[]) if a==sym}
            nxt=frozenset(epsilon_closure(trans,moved))
            if not nxt: continue
            if nxt not in ids: ids[nxt]=len(ids); q.append(nxt)
            table[(cid,sym)]=ids[nxt]
    return 0,accepting,table
def dfa_match(start,accepting,table,text):
    # PEDAGOGY-SOLUTION: D6-DFA-MATCH
    state=start
    for ch in text:
        key=(state,ch)
        if key not in table: return False
        state=table[key]
    return state in accepting
