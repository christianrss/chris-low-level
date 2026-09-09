class LiteralDFA:
    def __init__(self,pattern):
        # PEDAGOGY-SOLUTION: D7-GREP-DFA
        self.pattern=pattern;self.accept=len(pattern);self.trans={(i,ch):i+1 for i,ch in enumerate(pattern)}
    def fullmatch_at(self,text,start):
        if self.accept==0:return True
        state=0
        for ch in text[start:]:
            key=(state,ch)
            if key not in self.trans:return False
            state=self.trans[key]
            if state==self.accept:return True
        return False
    def contains(self,text):
        # PEDAGOGY-SOLUTION: D7-GREP-SEARCH
        return any(self.fullmatch_at(text,i) for i in range(len(text)+1))
def grep_file(path,pattern):
    # PEDAGOGY-SOLUTION: D7-GREP-FILE
    dfa=LiteralDFA(pattern);out=[]
    with open(path,"r",encoding="utf-8",errors="replace") as f:
        for n,line in enumerate(f,1):
            if dfa.contains(line):out.append((n,line.rstrip("\n")))
    return out
