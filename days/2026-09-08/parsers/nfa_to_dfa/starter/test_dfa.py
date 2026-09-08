from dfa import *
# NFA for a*
trans={0:[(None,1),(None,3)],1:[("a",2)],2:[(None,1),(None,3)],3:[]}
# PEDAGOGY-TEST: D6-DFA-CLOSURE
assert epsilon_closure(trans,{0})=={0,1,3}
# PEDAGOGY-TEST: D6-DFA-SUBSET
s,a,t=subset_construct(trans,0,3); assert s in a
# PEDAGOGY-TEST: D6-DFA-MATCH
assert dfa_match(s,a,t,"") and dfa_match(s,a,t,"aaaa") and not dfa_match(s,a,t,"b")
print("chris-dfa tests passed")
