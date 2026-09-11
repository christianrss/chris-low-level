from import_name_triage import normalize_name, flag_suspicious, triage_score
# PEDAGOGY-TEST: RT-IMP-01
def test_norm():
    assert normalize_name("  VirtualAlloc ") == "VirtualAlloc"
    try:
        normalize_name("   ")
        assert False
    except ValueError:
        pass
# PEDAGOGY-TEST: RT-IMP-02
def test_flag():
    assert flag_suspicious(["MessageBoxA", "VirtualAlloc", "foo"]) == ["VirtualAlloc"]
# PEDAGOGY-TEST: RT-IMP-03
def test_score():
    assert triage_score(["VirtualAlloc", "CreateRemoteThread"]) == 20

if __name__ == "__main__":
    test_norm(); test_flag(); test_score(); print("ok")
