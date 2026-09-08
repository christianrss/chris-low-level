from bm25 import *
docs={"allocator.cpp":"slab allocator allocate free slot","tensor.cpp":"tensor matmul stride kernel","alloc_test.cpp":"allocator test free allocation"}
# PEDAGOGY-TEST: D6-BM25-TOKENIZE
assert tokenize("Foo_bar(x)")[:1]==["foo_bar"]
# PEDAGOGY-TEST: D6-BM25-INDEX
m=BM25(docs); assert m.df["allocator"]==2
# PEDAGOGY-TEST: D6-BM25-SCORE
r=m.rank("slab allocator"); assert r[0]=="allocator.cpp"
# PEDAGOGY-TEST: D6-BM25-EVAL
assert reciprocal_rank(r,{"allocator.cpp"})==1.0
print("chris-bm25 tests passed")
