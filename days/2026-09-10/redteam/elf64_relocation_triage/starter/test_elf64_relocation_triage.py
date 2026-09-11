from elf64_relocation_triage import triage

def test_elf():
    # PEDAGOGY-TEST: D8-ELF-MAGIC
    # PEDAGOGY-TEST: D8-ELF-CLASS
    # PEDAGOGY-TEST: D8-ELF-RELOC
    blob = b"\x7fELF" + bytes([2, 3])
    r = triage(blob)
    assert r["ok"] and r["relocs"] == 3
    assert triage(b"MZ")["ok"] is False
