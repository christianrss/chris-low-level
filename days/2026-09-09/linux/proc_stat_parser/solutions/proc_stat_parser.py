def parse_stat(text):
    # PEDAGOGY-SOLUTION: D7-PROC-PREFIX
    lp = text.find("(")
    rp = text.rfind(")")
    if lp < 0 or rp < lp:
        raise ValueError("format")
    pid = int(text[:lp].strip())
    comm = text[lp+1:rp]
    # PEDAGOGY-SOLUTION: D7-PROC-FIELDS
    rest = text[rp+2:].split()
    if len(rest) < 20:
        raise ValueError("truncated")
    return {
        "pid": pid,
        "comm": comm,
        "state": rest[0],
        "ppid": int(rest[1]),
        "utime": int(rest[11]),
        "stime": int(rest[12]),
        "num_threads": int(rest[17]),
        "starttime": int(rest[19]),
    }

def read_self():
    # PEDAGOGY-SOLUTION: D7-PROC-SELF
    # lab: parse fixture string instead of real /proc on Windows
    fixture = "1 (init) S 0 0 0 0 0 0 0 0 0 0 0 10 20 0 0 0 0 1 0 100"
    return parse_stat(fixture)
