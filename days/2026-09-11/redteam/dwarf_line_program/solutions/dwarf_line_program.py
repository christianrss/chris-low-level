def read_uleb(data,off):
    # PEDAGOGY-SOLUTION: D9-DWARF-ULEB
    value=0;shift=0
    for _ in range(10):
        if off>=len(data): raise ValueError("truncated uleb")
        b=data[off];off+=1;value|=(b&0x7f)<<shift
        if not b&0x80:return value,off
        shift+=7
    raise ValueError("uleb too long")
def read_sleb(data,off):
    # PEDAGOGY-SOLUTION: D9-DWARF-SLEB
    value=0;shift=0
    for _ in range(10):
        if off>=len(data): raise ValueError("truncated sleb")
        b=data[off];off+=1;value|=(b&0x7f)<<shift;shift+=7
        if not b&0x80:
            if shift<64 and b&0x40:value|=-(1<<shift)
            return value,off
    raise ValueError("sleb too long")
def run_line_program(data):
    # PEDAGOGY-SOLUTION: D9-DWARF-VM
    pc=0;address=0;line=1;file=1;rows=[]
    while pc<len(data):
        op=data[pc];pc+=1
        if op==0:
            if pc!=len(data): raise ValueError("bytes after end")
            return rows
        if op==1:
            d,pc=read_uleb(data,pc); address+=d
        elif op==2:
            d,pc=read_sleb(data,pc); line+=d
            if line<=0: raise ValueError("line")
        elif op==3:
            file,pc=read_uleb(data,pc)
            if file==0: raise ValueError("file")
        elif op==4: rows.append((address,file,line))
        else: raise ValueError("opcode")
    raise ValueError("missing end")
