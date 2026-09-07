def parse_program_headers(data: bytes):
    # PEDAGOGY-SOLUTION: D5-ELF-HEADER
    if len(data)<64 or data[:4]!=b"\x7fELF" or data[4]!=2 or data[5]!=1: raise ValueError("invalid ELF64 LE")
    phoff=int.from_bytes(data[32:40],"little"); ents=int.from_bytes(data[54:56],"little"); num=int.from_bytes(data[56:58],"little")
    if ents<56 or phoff+ents*num>len(data): raise ValueError("truncated phdr table")
    out=[]
    for i in range(num):
        # PEDAGOGY-SOLUTION: D5-ELF-PHDR
        o=phoff+i*ents
        typ=int.from_bytes(data[o:o+4],"little"); flags=int.from_bytes(data[o+4:o+8],"little")
        po=int.from_bytes(data[o+8:o+16],"little"); va=int.from_bytes(data[o+16:o+24],"little")
        fs=int.from_bytes(data[o+32:o+40],"little"); ms=int.from_bytes(data[o+40:o+48],"little")
        al=int.from_bytes(data[o+48:o+56],"little")
        # PEDAGOGY-SOLUTION: D5-ELF-RANGE
        if po+fs>len(data): raise ValueError("segment outside file")
        if typ==1 and ms<fs: raise ValueError("PT_LOAD memsz < filesz")
        out.append(dict(type=typ,flags=flags,offset=po,vaddr=va,filesz=fs,memsz=ms,align=al))
    return out
