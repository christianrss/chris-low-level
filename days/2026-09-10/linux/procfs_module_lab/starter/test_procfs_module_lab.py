from procfs_module_lab import ProcFS
def test_proc():
    # PEDAGOGY-TEST: D8-PROC-WRITE
    # PEDAGOGY-TEST: D8-PROC-READ
    # PEDAGOGY-TEST: D8-PROC-LIST
    p = ProcFS(); p.write("stats", "1"); assert p.read("stats")=="1"; assert p.list()==["stats"]
