from query import *
# PEDAGOGY-TEST: D5-PRATT-LEX
assert lex('lang:cpp')[1][0]=="COL"
# PEDAGOGY-TEST: D5-PRATT-PARSE
assert parse("a OR b AND c")==("or",("text","a"),("and",("text","b"),("text","c")))
# PEDAGOGY-TEST: D5-PRATT-FIELD
assert parse('lang:cpp AND NOT text:"generated code"')[0]=="and"
print("chris-pratt-query tests passed")
