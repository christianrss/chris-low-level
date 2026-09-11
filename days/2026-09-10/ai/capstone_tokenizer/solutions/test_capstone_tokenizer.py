# PEDAGOGY-TEST: CAP-AI-TOK-01
# PEDAGOGY-TEST: CAP-AI-TOK-02
# PEDAGOGY-TEST: CAP-AI-TOK-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_tokenizer import bytes_to_ids, merge_runs, vocab_size

def main():
    ids = bytes_to_ids(b"aaab")
    assert ids == [97, 97, 97, 98]
    assert merge_runs(ids) == [(97, 3), (98, 1)]
    assert vocab_size(ids) == 2
    print("OK tokenizer")

if __name__ == "__main__":
    main()
