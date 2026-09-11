from dwarf_line_program import read_uleb, read_sleb, run_line_program

def test_uleb_sleb():
    # PEDAGOGY-TEST: D9-DWARF-ULEB
    # PEDAGOGY-TEST: D9-DWARF-SLEB
    v, o = read_uleb(bytes([0x80, 0x01]), 0)
    assert v == 128 and o == 2
    v, o = read_sleb(bytes([0x7f]), 0)
    assert v == -1

def test_vm():
    # PEDAGOGY-TEST: D9-DWARF-VM
    # op1 uleb2, op2 sleb+1, op4 row, op0 end
    prog = bytes([1, 2, 2, 1, 4, 0])
    rows = run_line_program(prog)
    assert rows == [(2, 1, 2)]
