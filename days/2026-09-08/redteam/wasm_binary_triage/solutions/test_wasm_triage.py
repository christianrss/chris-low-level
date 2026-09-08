from wasm_triage import *
data=b"\0asm\x01\0\0\0"+bytes([0,3])+b"abc"+bytes([1,1,0])
# PEDAGOGY-TEST: D6-WASM-HEADER
# PEDAGOGY-TEST: D6-WASM-ULEB
# PEDAGOGY-TEST: D6-WASM-SECTIONS
s=parse_sections(data); assert [(x["id"],x["payload_size"]) for x in s]==[(0,3),(1,1)]
ok=False
try: parse_sections(data[:-1])
except ValueError: ok=True
assert ok
print("chris-wasm-triage tests passed")
