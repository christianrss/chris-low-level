# PEDAGOGY-TEST: AI-EVT-ENT-01
# PEDAGOGY-TEST: AI-EVT-RLE-02
# PEDAGOGY-TEST: AI-EVT-RATIO-03
# Caso 1: entropy de bytes repetidos é baixa
# Caso 2: RLE em [1,1,2] -> [(1,2),(2,1)]
# Caso 3: gzip ratio < 1 em dados repetitivos
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from input_entropy import shannon_entropy_events, event_rle_encode, compression_ratio_gzip_events

def main():
    rep = bytes([1] * 240)
    assert shannon_entropy_events(rep) < 0.01
    assert event_rle_encode([1, 1, 2]) == [(1, 2), (2, 1)]
    assert compression_ratio_gzip_events(rep) < 0.5
    print("OK input_entropy")

if __name__ == "__main__":
    main()
