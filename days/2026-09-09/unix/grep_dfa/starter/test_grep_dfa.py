from pathlib import Path
from grep_dfa import LiteralDFA, grep_file

def test_dfa_search(tmp_path=None):
    # PEDAGOGY-TEST: D7-GREP-DFA
    # PEDAGOGY-TEST: D7-GREP-SEARCH
    d = LiteralDFA("ab")
    assert d.contains("xxabyy")
    assert not d.contains("a")

def test_file(tmp_path):
    # PEDAGOGY-TEST: D7-GREP-FILE
    p = tmp_path / "f.txt"
    p.write_text("one\nabc\nzzz\n", encoding="utf-8")
    hits = grep_file(str(p), "ab")
    assert hits == [(2, "abc")]
