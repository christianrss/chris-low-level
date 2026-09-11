"""Flag suspicious PE import names."""
SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread", "NtMapViewOfSection")

def normalize_name(name: str) -> str:
    # PEDAGOGY-SOLUTION: RT-IMP-01
    s = name.strip()
    if not s:
        raise ValueError("empty")
    return s

def flag_suspicious(names: list[str]) -> list[str]:
    # PEDAGOGY-SOLUTION: RT-IMP-02
    out = []
    for n in names:
        nn = normalize_name(n)
        if nn in SUSPICIOUS:
            out.append(nn)
    return out

def triage_score(names: list[str]) -> int:
    # PEDAGOGY-SOLUTION: RT-IMP-03
    return 10 * len(flag_suspicious(names))
