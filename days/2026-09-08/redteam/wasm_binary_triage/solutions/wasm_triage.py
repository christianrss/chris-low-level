def read_u32_leb(data,offset):
    # PEDAGOGY-SOLUTION: D6-WASM-ULEB
    value=0; shift=0
    for _ in range(5):
        if offset>=len(data): raise ValueError("truncated ULEB128")
        b=data[offset]; offset+=1; value |= (b&0x7f)<<shift
        if not (b&0x80): return value,offset
        shift+=7
    raise ValueError("ULEB128 too long")
def parse_sections(data):
    # PEDAGOGY-SOLUTION: D6-WASM-HEADER
    if len(data)<8 or data[:4]!=b"\0asm" or data[4:8]!=b"\x01\0\0\0": raise ValueError("bad WASM header")
    # PEDAGOGY-SOLUTION: D6-WASM-SECTIONS
    out=[]; cur=8
    while cur<len(data):
        h=cur; sid=data[cur]; cur+=1
        size,cur=read_u32_leb(data,cur); end=cur+size
        if end>len(data): raise ValueError("truncated section")
        out.append({"id":sid,"header_offset":h,"payload_offset":cur,"payload_size":size})
        cur=end
    return out
