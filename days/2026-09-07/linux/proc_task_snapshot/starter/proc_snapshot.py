from dataclasses import dataclass
@dataclass(frozen=True)
class Task: pid:int; comm:str; state:str; ppid:int; utime:int; stime:int; num_threads:int; starttime:int
def parse_stat(line):
    # TODO [D5-PROC-PARSE]: parseie /proc/<pid>/stat sem split ingênuo do comm.
    raise NotImplementedError
def scan(root="/proc"):
    # TODO [D5-PROC-SCAN]: enumere PIDs tolerando races.
    return {}
def cpu_ticks_delta(a,b):
    # TODO [D5-PROC-DELTA]: delta apenas se identidade do processo é a mesma.
    return 0
