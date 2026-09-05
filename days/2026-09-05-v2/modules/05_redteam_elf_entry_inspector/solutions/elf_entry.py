# SOLVES [RT-ELF-HDR-01] [RT-ELF-ENTRY-02]
import struct
def parse_ident(data:bytes):
    if len(data)<16: raise ValueError('truncated ident')
    if data[:4]!=b'\x7fELF': raise ValueError('bad magic')
    if data[4]!=2: raise ValueError('not ELF64')
    if data[5]!=1: raise ValueError('not little-endian')
    return {'class':64,'little_endian':True}
def parse_elf64(data:bytes):
    if len(data)<64: raise ValueError('truncated ELF64 header')
    parse_ident(data)
    e_type,e_machine,e_version,e_entry=struct.unpack_from('<HHIQ',data,16)
    return {'e_type':e_type,'e_machine':e_machine,'e_version':e_version,'e_entry':e_entry}
