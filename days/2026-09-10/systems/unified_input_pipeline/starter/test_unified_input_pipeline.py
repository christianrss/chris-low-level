# PEDAGOGY-TEST: CAP-INP-KBD-01
# PEDAGOGY-TEST: CAP-INP-MUX-02
# PEDAGOGY-TEST: CAP-INP-XFM-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from unified_input_pipeline import parse_keyboard_chunk, mux_streams, transform_events

def ev_key(code, val=1):
    b = bytearray(24)
    b[16:18] = (1).to_bytes(2, "little")
    b[18:20] = code.to_bytes(2, "little")
    b[20:24] = val.to_bytes(4, "little", signed=True)
    return bytes(b)

def main():
    kbd = parse_keyboard_chunk(ev_key(30))
    assert kbd == [(1, 30, 1)]
    muxed = mux_streams(kbd, [(2, 0, 5)])
    assert transform_events(muxed) == ["KEY:30", "REL:0=5"]
    print("OK unified_input")

if __name__ == "__main__":
    main()
