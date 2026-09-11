# PEDAGOGY-TEST: CAP-Q-MEAS-01
# PEDAGOGY-TEST: CAP-Q-MEAS-02
# PEDAGOGY-TEST: CAP-Q-MEAS-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_measurement import born_probability, collapse, measure_sample

def main():
    assert abs(born_probability(0.5+0.5j) - 0.5) < 1e-9
    c = collapse([1, 0], 1)
    assert c[1] == 1
    assert measure_sample([0.5, 0.5], 0.75) == 1
    print("OK quantum")

if __name__ == "__main__":
    main()
