# PEDAGOGY-TEST: CAP-PRATT-01
# PEDAGOGY-TEST: CAP-PRATT-02
# PEDAGOGY-TEST: CAP-PRATT-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_query_eval import lex, eval_query

def main():
    assert lex("a:1 AND b:2") == ["a:1", "AND", "b:2"]
    assert eval_query("a:1 AND b:2") is True
    assert eval_query("false OR true") is True
    print("OK pratt")

if __name__ == "__main__":
    main()
