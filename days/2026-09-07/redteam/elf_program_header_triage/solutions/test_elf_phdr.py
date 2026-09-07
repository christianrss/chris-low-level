from elf_phdr import parse_program_headers
def make():
 d=bytearray(256); d[:4]=b"\x7fELF"; d[4]=2; d[5]=1; d[32:40]=(64).to_bytes(8,"little"); d[54:56]=(56).to_bytes(2,"little"); d[56:58]=(2).to_bytes(2,"little")
 for i,(typ,po,fs,ms) in enumerate([(1,200,16,32),(4,216,8,8)]):
  o=64+i*56; d[o:o+4]=typ.to_bytes(4,"little"); d[o+4:o+8]=(5).to_bytes(4,"little"); d[o+8:o+16]=po.to_bytes(8,"little"); d[o+16:o+24]=(0x400000+i*0x1000).to_bytes(8,"little"); d[o+32:o+40]=fs.to_bytes(8,"little"); d[o+40:o+48]=ms.to_bytes(8,"little"); d[o+48:o+56]=(0x1000).to_bytes(8,"little")
 return bytes(d)
d=make()
# PEDAGOGY-TEST: D5-ELF-HEADER
# PEDAGOGY-TEST: D5-ELF-PHDR
x=parse_program_headers(d); assert len(x)==2 and x[0]["type"]==1
# PEDAGOGY-TEST: D5-ELF-RANGE
b=bytearray(d); b[64+8:64+16]=(250).to_bytes(8,"little"); b[64+32:64+40]=(16).to_bytes(8,"little")
try: parse_program_headers(bytes(b)); assert False
except ValueError: pass
print("chris-elf-phdr tests passed")
