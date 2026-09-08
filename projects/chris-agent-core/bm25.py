import re,math
from collections import Counter
def tokenize(text):
    # PEDAGOGY-SOLUTION: D6-BM25-TOKENIZE
    return [x.lower() for x in re.findall(r"[A-Za-z_][A-Za-z0-9_]*",text)]
class BM25:
    def __init__(self,docs):
        # PEDAGOGY-SOLUTION: D6-BM25-INDEX
        self.docs=docs; self.toks={p:tokenize(t) for p,t in docs.items()}; self.tf={p:Counter(ts) for p,ts in self.toks.items()}
        self.df=Counter()
        for ts in self.toks.values():
            for term in set(ts): self.df[term]+=1
        self.N=len(docs); self.avgdl=sum(map(len,self.toks.values()))/max(1,self.N)
    def rank(self,query):
        # PEDAGOGY-SOLUTION: D6-BM25-SCORE
        q=tokenize(query); k1=1.2; b=.75; out=[]
        for p,tfm in self.tf.items():
            dl=len(self.toks[p]); score=0.0
            for term in q:
                if not tfm[term]: continue
                df=self.df[term]; idf=math.log(1+(self.N-df+.5)/(df+.5)); tf=tfm[term]
                score += idf*(tf*(k1+1))/(tf+k1*(1-b+b*dl/self.avgdl))
            if score>0: out.append((p,score))
        return [p for p,_ in sorted(out,key=lambda x:(-x[1],x[0]))]
def reciprocal_rank(ranked,relevant):
    # PEDAGOGY-SOLUTION: D6-BM25-EVAL
    for i,p in enumerate(ranked,1):
        if p in relevant: return 1.0/i
    return 0.0
