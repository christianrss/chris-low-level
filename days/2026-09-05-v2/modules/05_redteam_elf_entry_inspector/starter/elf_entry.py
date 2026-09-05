import struct

def parse_ident(data: bytes):
    # TODO [RT-ELF-HDR-01]: validar magic, classe ELF64 e little-endian
    raise NotImplementedError

def parse_elf64(data: bytes):
    # TODO [RT-ELF-ENTRY-02]: extrair e_type, e_machine, e_version e e_entry
    raise NotImplementedError
