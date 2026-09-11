from proc_stat_parser import parse_stat, read_self

def test_prefix_fields():
    # PEDAGOGY-TEST: D7-PROC-PREFIX
    # PEDAGOGY-TEST: D7-PROC-FIELDS
    r = parse_stat("42 (my task) R 1 0 0 0 0 0 0 0 0 0 0 5 7 0 0 0 0 3 0 99")
    assert r["pid"] == 42 and r["comm"] == "my task" and r["state"] == "R"
    assert r["utime"] == 5 and r["stime"] == 7 and r["num_threads"] == 3

def test_self():
    # PEDAGOGY-TEST: D7-PROC-SELF
    r = read_self()
    assert r["pid"] == 1 and r["comm"] == "init"
