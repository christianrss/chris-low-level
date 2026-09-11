"""Flag suspicious PE import names."""
SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread", "NtMapViewOfSection")

def normalize_name(name: str) -> str:
    # TODO [RT-IMP-01]: strip whitespace; reject empty
    raise NotImplementedError("RT-IMP-01")

def flag_suspicious(names: list[str]) -> list[str]:
    # TODO [RT-IMP-02]: return names in SUSPICIOUS (preserve order)
    raise NotImplementedError("RT-IMP-02")

def triage_score(names: list[str]) -> int:
    # TODO [RT-IMP-03]: 10 points per flagged name
    raise NotImplementedError("RT-IMP-03")
