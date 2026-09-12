import sys

KNOWN = {"MUTANT-01", "MUTANT-02"}
raise SystemExit(0 if len(sys.argv) == 2 and sys.argv[1] in KNOWN else 1)
