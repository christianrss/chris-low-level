from x86_prologue_triage import triage

def test_push_mov_stack():
    # PEDAGOGY-TEST: D7-X86-PUSH
    # PEDAGOGY-TEST: D7-X86-MOV
    # PEDAGOGY-TEST: D7-X86-STACK
    blob = bytes([0x55, 0x48, 0x89, 0xe5, 0x48, 0x83, 0xec, 0x20])
    r = triage(blob)
    assert r["push_rbp"] and r["frame_pointer"] and r["stack_reserve"] == 0x20 and r["consumed"] == 8
