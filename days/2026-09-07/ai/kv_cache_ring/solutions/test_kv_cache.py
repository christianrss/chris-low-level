from kv_cache import KVCacheRing
c=KVCacheRing(3)
# PEDAGOGY-TEST: D5-KV-APPEND
for p in range(4): c.append(p,f"k{p}",f"v{p}")
assert c.next_position==4
# PEDAGOGY-TEST: D5-KV-WINDOW
assert c.window(1,4)==[("k1","v1"),("k2","v2"),("k3","v3")]
try: c.window(0,1); assert False
except KeyError: pass
# PEDAGOGY-TEST: D5-KV-RESET
c.reset(); assert c.next_position==0 and c.positions==[None]*3
print("chris-kv-cache tests passed")
