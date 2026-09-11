# PEDAGOGY-TEST: CAP-LNX-COMP-01
# PEDAGOGY-TEST: CAP-LNX-EVDEV-02
# PEDAGOGY-TEST: CAP-LNX-SYNC-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from composite_input_driver import register_device, hid_boot_to_evdev, finalize_frame

def main():
    dev = register_device("composite0", {"EV_KEY", "EV_REL"})
    assert dev["name"] == "composite0"
    ev = hid_boot_to_evdev(bytes([0, 0, 4, 0, 0, 0, 0, 0]))
    assert ev == [(1, 4, 1)]
    frame = finalize_frame(ev)
    assert frame[-1] == (0, 0, 0)
    print("OK composite_input")

if __name__ == "__main__":
    main()
