#!/usr/bin/env python3
"""CLI tests for clvm-xdbg. CTest passes the binary and this source tree."""

from __future__ import annotations

import struct
import subprocess
import sys
import tempfile
from pathlib import Path

# PEDAGOGY-TEST: XDBG-LOAD-01
# PEDAGOGY-TEST: XDBG-HEX-01
# PEDAGOGY-TEST: XDBG-DISASM-01
# PEDAGOGY-TEST: XDBG-STEP-01
# PEDAGOGY-TEST: XDBG-REGS-01
# PEDAGOGY-TEST: XDBG-MEM-01
# PEDAGOGY-TEST: XDBG-BREAK-01
# PEDAGOGY-TEST: XDBG-ERR-01

EXE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("clvm-xdbg")
ROOT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1]
ASSEMBLE = ROOT / "tools" / "assemble.py"
PROGRAMS = ROOT / "programs"


def fnv1a32(data: bytes) -> int:
    hash_value = 0x811C9DC5
    for byte in data:
        hash_value ^= byte
        hash_value = (hash_value * 0x01000193) & 0xFFFFFFFF
    return hash_value


def wrap(code: bytes) -> bytes:
    checksum = fnv1a32(code)
    header = b"CLVM" + bytes([1, 0]) + struct.pack("<HII", 0, len(code), checksum)
    return header + code


def assemble_program(name: str, dest: Path) -> Path:
    src = PROGRAMS / name
    subprocess.check_call([sys.executable, str(ASSEMBLE), str(src), str(dest)])
    return dest


def run_dbg(image: Path, commands: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    payload = "\n".join(commands) + "\n"
    return subprocess.run(
        [str(EXE), str(image)],
        input=payload,
        capture_output=True,
        text=True,
        check=check,
    )


def combined(proc: subprocess.CompletedProcess[str]) -> str:
    return (proc.stdout or "") + (proc.stderr or "")


def test_load_valid_add2() -> None:
    # Caso 1
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["quit"])
        text = combined(proc)
        assert proc.returncode == 0, text
        assert "ready pc=0" in text, text


def test_hex_header_and_code() -> None:
    # Caso 2
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["hex", "quit"])
        text = combined(proc)
        assert "43 4C 56 4D" in text.upper().replace("43 4c 56 4d", "43 4C 56 4D"), text
        assert "header" in text, text
        assert "code" in text, text
        assert "0000" in text, text
        assert "0010" in text, text


def test_disasm_push_at_entry() -> None:
    # Caso 3
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["disasm", "quit"])
        text = combined(proc)
        assert "pc=0" in text, text
        assert "PUSH" in text, text
        assert "3" in text, text


def test_disasm_call_operand() -> None:
    # Caso 4
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["step", "step", "disasm", "quit"])
        text = combined(proc)
        assert "CALL" in text, text
        assert "2" in text, text


def test_step_push_updates_stack() -> None:
    # Caso 5
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["step", "regs", "quit"])
        text = combined(proc)
        assert "data=[3]" in text, text
        assert "pc=5" in text, text


def test_regs_shows_pc_and_stacks() -> None:
    # Caso 6
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["step", "step", "step", "regs", "quit"])
        text = combined(proc)
        assert "data=[3,5]" in text, text
        assert "call=[13]" in text, text
        assert "status=ready" in text, text


def test_mem_view_after_store() -> None:
    # Caso 7
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("mem_demo.asm", Path(raw) / "mem.clvm")
        proc = run_dbg(image, ["step", "step", "step", "mem 0 4", "quit"])
        text = combined(proc)
        assert "2A 00 00 00" in text.upper().replace("2a 00 00 00", "2A 00 00 00"), text


def test_breakpoint_stops_before_print() -> None:
    # Caso 8
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["break 13", "continue", "regs", "disasm", "quit"])
        text = combined(proc)
        assert "status=breakpoint" in text, text
        assert "pc=13" in text, text
        assert "prints=[]" in text, text
        assert "PRINT" in text, text


def test_continue_to_halt() -> None:
    # Caso 9
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        proc = run_dbg(image, ["continue", "regs", "quit"])
        text = combined(proc)
        assert "status=halted" in text, text
        assert "prints=[8]" in text, text


def test_e2e_add2_prints_8() -> None:
    # Caso 10
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("add2.asm", Path(raw) / "add2.clvm")
        commands = ["step"] * 8 + ["regs", "quit"]
        proc = run_dbg(image, commands)
        text = combined(proc)
        assert "prints=[8]" in text, text
        assert "status=halted" in text, text


def test_truncated_image() -> None:
    # Caso 11
    with tempfile.TemporaryDirectory() as raw:
        image = Path(raw) / "short.clvm"
        image.write_bytes(b"CLVM\x01\x00\x00\x00")
        proc = run_dbg(image, ["quit"])
        text = combined(proc)
        assert proc.returncode != 0, text
        assert "file too small" in text, text


def test_unknown_opcode() -> None:
    # Caso 12
    with tempfile.TemporaryDirectory() as raw:
        image = Path(raw) / "badop.clvm"
        image.write_bytes(wrap(bytes([0xFF])))
        proc = run_dbg(image, ["step", "quit"])
        text = combined(proc)
        assert "unknown opcode" in text, text
        assert "status=error" in text, text


def test_stack_underflow() -> None:
    # Caso 13
    with tempfile.TemporaryDirectory() as raw:
        image = Path(raw) / "under.clvm"
        image.write_bytes(wrap(bytes([0x07, 0x08])))
        proc = run_dbg(image, ["step", "quit"])
        text = combined(proc)
        assert "stack underflow" in text, text


def test_memory_out_of_bounds() -> None:
    # Caso 14
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("bad_mem.asm", Path(raw) / "bad_mem.clvm")
        proc = run_dbg(image, ["continue", "quit"])
        text = combined(proc)
        assert "memory out of bounds" in text, text


def test_return_stack_underflow() -> None:
    # Caso 15
    with tempfile.TemporaryDirectory() as raw:
        image = assemble_program("bad_ret.asm", Path(raw) / "bad_ret.clvm")
        proc = run_dbg(image, ["step", "quit"])
        text = combined(proc)
        assert "return stack underflow" in text, text


def main() -> int:
    tests = [
        test_load_valid_add2,
        test_hex_header_and_code,
        test_disasm_push_at_entry,
        test_disasm_call_operand,
        test_step_push_updates_stack,
        test_regs_shows_pc_and_stacks,
        test_mem_view_after_store,
        test_breakpoint_stops_before_print,
        test_continue_to_halt,
        test_e2e_add2_prints_8,
        test_truncated_image,
        test_unknown_opcode,
        test_stack_underflow,
        test_memory_out_of_bounds,
        test_return_stack_underflow,
    ]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001 — surface the first assertion
            print(f"FAIL {test.__name__}: {exc}")
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
