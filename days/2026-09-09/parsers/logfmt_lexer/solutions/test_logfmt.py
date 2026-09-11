# PEDAGOGY-TEST: PR-LOGFMT-LEX-01
# PEDAGOGY-TEST: PR-LOGFMT-KV-02
# PEDAGOGY-TEST: PR-LOGFMT-ESC-03
# Caso 1: 2 tokens
# Caso 2: msg=hello
# Caso 3: level=info
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from logfmt import tokenize, parse_kv, parse_line

def main():
    assert len(tokenize("a=1 b=2")) == 2
    assert parse_kv("msg=hello") == ("msg", "hello")
    d = parse_line('level=info msg="hello world"')
    assert d["level"] == "info"
    print("OK logfmt")

if __name__ == "__main__":
    main()
