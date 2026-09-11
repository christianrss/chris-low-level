def triage(data: bytes):
    # PEDAGOGY-SOLUTION: D8-ELF-MAGIC
    if data[:4] != b"\x7fELF":
        return {"ok": False, "reason": "magic"}
    # PEDAGOGY-SOLUTION: D8-ELF-CLASS
    if len(data) < 5 or data[4] != 2:
        return {"ok": False, "reason": "class"}
    # PEDAGOGY-SOLUTION: D8-ELF-RELOC
    # synthetic: byte 5 = reloc count
    n = data[5] if len(data) > 5 else 0
    return {"ok": True, "class": 64, "relocs": n}
