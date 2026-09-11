# PEDAGOGY-TEST: LX-PERF-OPEN-01
# PEDAGOGY-TEST: LX-PERF-READ-02
# PEDAGOGY-TEST: LX-PERF-CLOSE-03
# Caso 1: handle positivo
# Caso 2: read retorna 42
# Caso 3: close retorna True
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from perf_lab import perf_event_open, perf_event_read, perf_event_close

def main():
    fd = perf_event_open(1, 2)
    assert fd > 0
    counters = {fd: 42}
    assert perf_event_read(fd, counters) == 42
    assert perf_event_close(fd, counters) is True
    assert fd not in counters
    print("OK perf_lab")

if __name__ == "__main__":
    main()
