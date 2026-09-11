from context_budgeter import base_score, pack

def test_score_pack():
    # PEDAGOGY-TEST: D9-CTX-SCORE
    # PEDAGOGY-TEST: D9-CTX-DEDUPE
    # PEDAGOGY-TEST: D9-CTX-DIVERSITY
    # PEDAGOGY-TEST: D9-CTX-BUDGET
    c = {"path": "a.py", "content": "x", "bytes": 1, "lexical": 1, "semantic": 1, "graph": 1}
    assert abs(base_score(c) - 1.0) < 1e-9
    out = pack([c, dict(c)], 10)
    assert len(out["selected"]) == 1
