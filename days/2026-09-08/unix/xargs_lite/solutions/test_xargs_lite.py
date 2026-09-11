from xargs_lite import *
# PEDAGOGY-TEST: D6-XARGS-SPLIT
assert split_items("a b\nc")==["a","b","c"]; assert split_items("one\0two words\0",True)==["one","two words"]
# PEDAGOGY-TEST: D6-XARGS-BATCH
assert batches(["a","b","c"],2)==[["a","b"],["c"]]
# PEDAGOGY-TEST: D6-XARGS-RUN
import sys
assert run_batches([sys.executable,"-c","import sys; assert len(sys.argv)<=3"],["a","b","c"],2)==0
print("chris-xargs-lite tests passed")
