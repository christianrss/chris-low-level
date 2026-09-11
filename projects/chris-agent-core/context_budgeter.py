import hashlib
def base_score(c):
    # PEDAGOGY-SOLUTION: D9-CTX-SCORE
    return .45*c["lexical"]+.35*c["semantic"]+.20*c["graph"]
def pack(candidates,budget):
    # PEDAGOGY-SOLUTION: D9-CTX-DEDUPE
    unique=[];seen=set();trace=[]
    for c in candidates:
        norm="\n".join(line.rstrip() for line in c["content"].splitlines())
        h=hashlib.sha256(norm.encode()).hexdigest()
        if h in seen:trace.append({"path":c["path"],"decision":"duplicate"});continue
        seen.add(h);x=dict(c);x["_base"]=base_score(c);unique.append(x)
    # PEDAGOGY-SOLUTION: D9-CTX-DIVERSITY
    chosen=[];paths=set();used=0;remaining=unique[:]
    while remaining:
        best=max(remaining,key=lambda c:(c["_base"]+(0.05 if c["path"] not in paths else 0),-c["bytes"],c["path"]))
        remaining.remove(best);effective=best["_base"]+(0.05 if best["path"] not in paths else 0)
        # PEDAGOGY-SOLUTION: D9-CTX-BUDGET
        if used+best["bytes"]>budget:
            trace.append({"path":best["path"],"decision":"over_budget","effective":effective});continue
        chosen.append({k:v for k,v in best.items() if not k.startswith("_")});used+=best["bytes"];paths.add(best["path"])
        trace.append({"path":best["path"],"decision":"selected","effective":effective})
    return {"selected":chosen,"used":used,"trace":trace}
