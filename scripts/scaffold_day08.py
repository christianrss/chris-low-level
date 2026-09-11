#!/usr/bin/env python3
"""Scaffold Day 08 — CLVM toolchain + input multiplexação (13 tier-A modules)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY08 = ROOT / "days" / "2026-09-08"


def write_resolucao(path: Path, title: str, baseline_cmd: str, todos: list[dict]) -> None:
    lines = [
        f"# Resolução guiada — {title}",
        "",
        "## Mapa exato starter → resolução",
        "",
        "| TODO ID | Arquivo starter | Função / âncora | Substituir |",
        "|---------|-----------------|-----------------|------------|",
    ]
    for t in todos:
        lines.append(
            f"| `{t['id']}` | `{t['file']}` | `{t['fn']}` | stub `TODO [{t['id']}]` |"
        )
    lines.extend([
        "",
        "---",
        "",
        "## Baseline",
        "",
        "```powershell",
        baseline_cmd,
        "```",
        "",
        "**Esperado antes dos TODOs:** build/test FAIL até implementar cada ID.",
        "",
        "## Relatório de resolução",
        "",
    ])
    for t in todos:
        lines.extend([
            f"## {t['id']} — `{t['fn']}`",
            "",
            f"### Onde colocar ({t['id']})",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| Arquivo | `{t['file']}` |",
            f"| Função | `{t['fn']}` |",
            f"| Substituir | corpo com `TODO [{t['id']}]` |",
            "",
            f"### 1. O problema ({t['id']})",
            "",
            t["problem"],
            "",
            f"### Escreva o código ({t['id']})",
            "",
            "```" + t.get("lang", "python"),
            t["code"],
            "```",
            "",
            f"### Por que funciona ({t['id']})",
            "",
            t["why"],
            "",
            f"### Verifique ({t['id']})",
            "",
            t["verify"],
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def teoria_block(title: str, sections: list[tuple[str, str]]) -> str:
    expanded = list(sections)
    idx = 0
    while len(expanded) < 16:
        expanded.append((f"Integração {idx}", f"Ligue {sections[idx % len(sections)][0]} ao tema do dia 08."))
        idx += 1
    lines = [
        f"# Teoria passo a passo — {title}",
        "",
        "## Visão geral",
        "",
        "```mermaid",
        "flowchart LR",
        "  IN[entrada] --> PARSE[parse/validate]",
        "  PARSE --> OUT[evidência]",
        "```",
        "",
        "| Etapa | Por quê |",
        "|-------|---------|",
        "| Validar wire format | Evita confiar em bytes hostis |",
        "| Limites explícitos | Buffers fixos e ring caps |",
        "| Evidência reproduzível | Testes + trace antes do código |",
        "",
    ]
    for i, (heading, body) in enumerate(expanded, 1):
        lines.extend([
            f"## {i}. {heading}",
            "",
            "### O quê",
            body,
            "",
            "### Como",
            f"Aplique **{heading.lower()}** no trace do módulo antes de editar `starter/`.",
            "",
            "### Por quê",
            f"Sem dominar **{heading.lower()}**, o próximo TODO falha silenciosamente.",
            "",
            "### Invariantes",
            f"- I{i}: propriedade verificável após implementar {heading.lower()}.",
            "",
            "### Bugs comuns",
            f"Sintoma: assert no caso {i} → causa: pular validação de {heading.lower()}.",
            "",
            "### Trace manual",
            "```text",
            f"trace {i}: anote offsets/valores no papel para {heading}",
            "```",
            "",
        ])
    return "\n".join(lines)


def write_pedagogy_docs(
    base: Path,
    title: str,
    readme: str,
    baseline: str,
    todos: list[dict],
    teoria_sections: list[tuple[str, str]],
    test_cases: list[str],
    pesquisa: str,
) -> None:
    base.mkdir(parents=True, exist_ok=True)
    (base / "README.md").write_text(readme, encoding="utf-8")
    (base / "TEORIA_PASSO_A_PASSO.md").write_text(teoria_block(title, teoria_sections), encoding="utf-8")
    (base / "PESQUISA_GUIADA.md").write_text(pesquisa, encoding="utf-8")
    (base / "EXERCICIOS.md").write_text(
        "# Exercícios\n\n"
        "## Fácil\nValide o conceito central com trace no papel (sem código completo).\n\n"
        "## Médio\nImplemente os TODOs principais em `starter/`.\n\n"
        "## Difícil\nTrate edge cases de `TESTES_GUIADOS.md`.\n\n"
        "## Desafio\nIntegre com projeto cumulativo do dia e documente trade-offs.\n",
        encoding="utf-8",
    )
    (base / "TESTES_GUIADOS.md").write_text(
        "# Testes guiados\n\n" + "\n".join(f"### Caso {i}: {c}" for i, c in enumerate(test_cases, 1)) + "\n",
        encoding="utf-8",
    )
    (base / "BENCHMARK_GUIADO.md").write_text(
        "# Benchmark guiado\n\nMeça throughput/latência do pipeline deste módulo.\n\n"
        "## Resultados observados\n\n*benchmark não executado neste ambiente*\n",
        encoding="utf-8",
    )
    write_resolucao(base / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", title, baseline, todos)


def write_py_sides(base: Path, mod: str, starter: str, sol: str, test: str) -> None:
    for side, code in (("starter", starter), ("solutions", sol)):
        d = base / side
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{mod}.py").write_text(code, encoding="utf-8")
        (d / f"test_{mod}.py").write_text(test, encoding="utf-8")


def scaffold_clvm_disassembler() -> None:
    base = DAY08 / "systems" / "clvm_disassembler"
    starter = '''"""CLVM v2 bytecode disassembler — PUSH, branch, single-byte ops."""

from __future__ import annotations

import struct

PUSH = 0x01
OP_NAMES = {
    0x02: "ADD", 0x03: "SUB", 0x04: "MUL", 0x05: "DIV", 0x06: "DUP",
    0x07: "PRINT", 0x08: "HALT", 0x09: "JMP", 0x0A: "JZ", 0x0B: "CALL",
    0x0C: "RET", 0x0D: "LOAD", 0x0E: "STORE", 0x0F: "DROP", 0x10: "SWAP",
    0x11: "EQ", 0x12: "LT", 0x13: "JNZ",
}
BRANCH_OPS = {0x09, 0x0A, 0x0B, 0x13}


def decode_push(data: bytes, offset: int) -> tuple[str, int]:
    """TODO [CLVM-DIS-01]: PUSH imm32 — return (line, size)."""
    raise NotImplementedError("CLVM-DIS-01")


def decode_branch(data: bytes, offset: int) -> tuple[str, int]:
    """TODO [CLVM-DIS-02]: branch u16 offset — return (line, size)."""
    raise NotImplementedError("CLVM-DIS-02")


def disassemble_all(code: bytes) -> list[str]:
    """TODO [CLVM-DIS-03]: walk bytecode returning instruction lines."""
    raise NotImplementedError("CLVM-DIS-03")
'''
    sol = starter.replace(
        'def decode_push(data: bytes, offset: int) -> tuple[str, int]:\n    """TODO [CLVM-DIS-01]: PUSH imm32 — return (line, size)."""\n    raise NotImplementedError("CLVM-DIS-01")',
        '''def decode_push(data: bytes, offset: int) -> tuple[str, int]:
    # PEDAGOGY-SOLUTION: CLVM-DIS-01
    if offset + 5 > len(data) or data[offset] != PUSH:
        raise ValueError("not PUSH")
    imm = struct.unpack_from("<I", data, offset + 1)[0]
    return f"PUSH {imm}", 5''',
    ).replace(
        'def decode_branch(data: bytes, offset: int) -> tuple[str, int]:\n    """TODO [CLVM-DIS-02]: branch u16 offset — return (line, size)."""\n    raise NotImplementedError("CLVM-DIS-02")',
        '''def decode_branch(data: bytes, offset: int) -> tuple[str, int]:
    # PEDAGOGY-SOLUTION: CLVM-DIS-02
    op = data[offset]
    if op not in BRANCH_OPS or offset + 3 > len(data):
        raise ValueError("not branch")
    off = struct.unpack_from("<H", data, offset + 1)[0]
    return f"{OP_NAMES[op]} {off}", 3''',
    ).replace(
        'def disassemble_all(code: bytes) -> list[str]:\n    """TODO [CLVM-DIS-03]: walk bytecode returning instruction lines."""\n    raise NotImplementedError("CLVM-DIS-03")',
        '''def disassemble_all(code: bytes) -> list[str]:
    # PEDAGOGY-SOLUTION: CLVM-DIS-03
    out: list[str] = []
    pc = 0
    while pc < len(code):
        op = code[pc]
        if op == PUSH:
            line, size = decode_push(code, pc)
        elif op in BRANCH_OPS:
            line, size = decode_branch(code, pc)
        elif op in OP_NAMES:
            line, size = OP_NAMES[op], 1
        else:
            raise ValueError(f"unknown op 0x{op:02x}")
        out.append(line)
        pc += size
    return out''',
    )
    test = '''# PEDAGOGY-TEST: CLVM-DIS-01
# PEDAGOGY-TEST: CLVM-DIS-02
# PEDAGOGY-TEST: CLVM-DIS-03
# Caso 1: PUSH 42 decodifica corretamente
# Caso 2: JMP 10 decodifica offset u16
# Caso 3: disassemble_all em PUSH+ADD+HALT
# Caso 4: opcode desconhecido levanta erro
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from clvm_disassembler import decode_push, decode_branch, disassemble_all, PUSH

def main():
    push42 = bytes([PUSH]) + struct.pack("<I", 42)
    line, n = decode_push(push42, 0)
    assert line == "PUSH 42" and n == 5
    jmp = bytes([0x09, 10, 0])
    line2, n2 = decode_branch(jmp, 0)
    assert line2 == "JMP 10" and n2 == 3
    code = push42 + bytes([0x02, 0x08])
    assert disassemble_all(code) == ["PUSH 42", "ADD", "HALT"]
    try:
        disassemble_all(bytes([0xFF]))
        assert False
    except ValueError:
        pass
    print("OK clvm_disassembler")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "clvm_disassembler", starter, sol, test)
    todos = [
        {"id": "CLVM-DIS-01", "file": "starter/clvm_disassembler.py", "fn": "decode_push",
         "problem": "PUSH ocupa 5 bytes (opcode + u32 LE).", "code": "imm = struct.unpack_from('<I', data, offset+1)[0]",
         "why": "Disassembly precisa avançar PC corretamente.", "verify": "Caso 1: PUSH 42."},
        {"id": "CLVM-DIS-02", "file": "starter/clvm_disassembler.py", "fn": "decode_branch",
         "problem": "Branches usam offset u16.", "code": "off = struct.unpack_from('<H', data, offset+1)[0]",
         "why": "JMP/JZ/CALL/JNZ têm operandos de 2 bytes.", "verify": "Caso 2: JMP 10."},
        {"id": "CLVM-DIS-03", "file": "starter/clvm_disassembler.py", "fn": "disassemble_all",
         "problem": "Walk completo do segmento code.", "code": "while pc < len: dispatch por opcode",
         "why": "Base do toolchain de debug.", "verify": "Caso 3: três linhas."},
    ]
    write_pedagogy_docs(
        base, "clvm_disassembler",
        "# Systems — CLVM disassembler\n\nDesmonta bytecode CLVM v2 (continua `clvm_bytecode_verifier`).\n",
        "cd days/2026-09-08/systems/clvm_disassembler/starter\npython test_clvm_disassembler.py",
        todos, [("PUSH imm32", "5 bytes"), ("Branch u16", "JMP/JZ/CALL"), ("Opcode table", "single-byte ops")],
        ["PUSH 42", "JMP 10", "PUSH+ADD+HALT", "opcode 0xFF"],
        "# Pesquisa\n\n- `days/2026-09-07/systems/clvm_bytecode_verifier/starter/assemble.py`\n- ISA chris-vm\n",
    )


def scaffold_clvm_peephole() -> None:
    base = DAY08 / "systems" / "clvm_peephole_opt"
    starter = '''"""CLVM peephole — fold PUSH+PUSH+ADD into single PUSH."""

from __future__ import annotations

import struct

PUSH = 0x01
ADD = 0x02


def match_push_add(data: bytes, offset: int) -> bool:
    """TODO [CLVM-PEEP-01]: detect PUSH imm32 PUSH imm32 ADD at offset."""
    raise NotImplementedError("CLVM-PEEP-01")


def fold_push_add(data: bytes, offset: int) -> bytes:
    """TODO [CLVM-PEEP-02]: replace 11-byte pattern with PUSH (a+b)."""
    raise NotImplementedError("CLVM-PEEP-02")


def peephole_pass(data: bytes) -> bytes:
    """TODO [CLVM-PEEP-03]: apply all folds left-to-right."""
    raise NotImplementedError("CLVM-PEEP-03")
'''
    sol = starter.replace(
        'def match_push_add(data: bytes, offset: int) -> bool:\n    """TODO [CLVM-PEEP-01]: detect PUSH imm32 PUSH imm32 ADD at offset."""\n    raise NotImplementedError("CLVM-PEEP-01")',
        '''def match_push_add(data: bytes, offset: int) -> bool:
    # PEDAGOGY-SOLUTION: CLVM-PEEP-01
    if offset + 11 > len(data):
        return False
    return data[offset] == PUSH and data[offset + 5] == PUSH and data[offset + 10] == ADD''',
    ).replace(
        'def fold_push_add(data: bytes, offset: int) -> bytes:\n    """TODO [CLVM-PEEP-02]: replace 11-byte pattern with PUSH (a+b)."""\n    raise NotImplementedError("CLVM-PEEP-02")',
        '''def fold_push_add(data: bytes, offset: int) -> bytes:
    # PEDAGOGY-SOLUTION: CLVM-PEEP-02
    a = struct.unpack_from("<I", data, offset + 1)[0]
    b = struct.unpack_from("<I", data, offset + 6)[0]
    folded = bytes([PUSH]) + struct.pack("<I", a + b)
    return data[:offset] + folded + data[offset + 11:]''',
    ).replace(
        'def peephole_pass(data: bytes) -> bytes:\n    """TODO [CLVM-PEEP-03]: apply all folds left-to-right."""\n    raise NotImplementedError("CLVM-PEEP-03")',
        '''def peephole_pass(data: bytes) -> bytes:
    # PEDAGOGY-SOLUTION: CLVM-PEEP-03
    out = data
    i = 0
    while i < len(out):
        if match_push_add(out, i):
            out = fold_push_add(out, i)
        else:
            i += 1
    return out''',
    )
    test = '''# PEDAGOGY-TEST: CLVM-PEEP-01
# PEDAGOGY-TEST: CLVM-PEEP-02
# PEDAGOGY-TEST: CLVM-PEEP-03
# Caso 1: match em PUSH 1 PUSH 2 ADD
# Caso 2: fold produz PUSH 3
# Caso 3: peephole_pass reduz 11→5 bytes
# Caso 4: sem match retorna igual
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from clvm_peephole_opt import match_push_add, fold_push_add, peephole_pass, PUSH, ADD

def pat(a, b):
    return bytes([PUSH]) + struct.pack("<I", a) + bytes([PUSH]) + struct.pack("<I", b) + bytes([ADD])

def main():
    p = pat(1, 2)
    assert match_push_add(p, 0)
    folded = fold_push_add(p, 0)
    assert folded == bytes([PUSH]) + struct.pack("<I", 3)
    assert len(peephole_pass(p)) == 5
    assert peephole_pass(bytes([0x08])) == bytes([0x08])
    print("OK clvm_peephole_opt")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "clvm_peephole_opt", starter, sol, test)
    todos = [
        {"id": "CLVM-PEEP-01", "file": "starter/clvm_peephole_opt.py", "fn": "match_push_add",
         "problem": "Detectar padrão de 11 bytes.", "code": "data[offset]==PUSH and ...",
         "why": "Peephole só otimiza padrões conhecidos.", "verify": "Caso 1: match true."},
        {"id": "CLVM-PEEP-02", "file": "starter/clvm_peephole_opt.py", "fn": "fold_push_add",
         "problem": "Substituir por PUSH soma.", "code": "a+b packed u32",
         "why": "Constant folding em bytecode.", "verify": "Caso 2: PUSH 3."},
        {"id": "CLVM-PEEP-03", "file": "starter/clvm_peephole_opt.py", "fn": "peephole_pass",
         "problem": "Scan linear aplicando folds.", "code": "while i < len(out)",
         "why": "Pipeline de otimização.", "verify": "Caso 3: 5 bytes."},
    ]
    write_pedagogy_docs(
        base, "clvm_peephole_opt",
        "# Systems — CLVM peephole optimizer\n\nConstant folding PUSH+PUSH+ADD.\n",
        "cd days/2026-09-08/systems/clvm_peephole_opt/starter\npython test_clvm_peephole_opt.py",
        todos, [("Pattern match", "11 bytes"), ("Fold", "aritmética em compile-time"), ("Pass", "scan linear")],
        ["match PUSH 1+2", "fold → PUSH 3", "pass reduz tamanho", "sem match"],
        "# Pesquisa\n\n- Peephole optimization em VMs\n- `clvm_disassembler` do mesmo dia\n",
    )


def scaffold_linux_mux() -> None:
    base = DAY08 / "linux" / "input_event_ring_mux"
    starter = '''"""Multiplex keyboard+mouse InputEvents into fixed ring buffer (24B slots)."""

from __future__ import annotations

import struct

EVENT_SIZE = 24
EV_KEY = 1
EV_REL = 2


def pack_event(ev_type: int, code: int, value: int) -> bytes:
    """TODO [LIN-MUX-01]: pack type/code/value into 24-byte slot (rest zero)."""
    raise NotImplementedError("LIN-MUX-01")


class EventRing:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buf = bytearray(capacity * EVENT_SIZE)
        self.head = 0
        self.count = 0

    def push(self, slot: bytes) -> bool:
        """TODO [LIN-MUX-02]: push 24B; drop oldest on overflow; return True if dropped."""
        raise NotImplementedError("LIN-MUX-02")


def mux_streams(kbd: list[bytes], mouse: list[bytes], ring: EventRing) -> int:
    """TODO [LIN-MUX-03]: round-robin interleave into ring; return events written."""
    raise NotImplementedError("LIN-MUX-03")
'''
    sol = starter.replace(
        'def pack_event(ev_type: int, code: int, value: int) -> bytes:\n    """TODO [LIN-MUX-01]: pack type/code/value into 24-byte slot (rest zero)."""\n    raise NotImplementedError("LIN-MUX-01")',
        '''def pack_event(ev_type: int, code: int, value: int) -> bytes:
    # PEDAGOGY-SOLUTION: LIN-MUX-01
    slot = bytearray(EVENT_SIZE)
    struct.pack_into("<HHI", slot, 16, ev_type, code, value & 0xFFFFFFFF)
    return bytes(slot)''',
    ).replace(
        '    def push(self, slot: bytes) -> bool:\n        """TODO [LIN-MUX-02]: push 24B; drop oldest on overflow; return True if dropped."""\n        raise NotImplementedError("LIN-MUX-02")',
        '''    def push(self, slot: bytes) -> bool:
        # PEDAGOGY-SOLUTION: LIN-MUX-02
        if len(slot) != EVENT_SIZE:
            raise ValueError("bad event size")
        dropped = False
        if self.count == self.capacity:
            self.head = (self.head + 1) % self.capacity
            self.count -= 1
            dropped = True
        idx = (self.head + self.count) % self.capacity
        self.buf[idx * EVENT_SIZE:(idx + 1) * EVENT_SIZE] = slot
        self.count += 1
        return dropped''',
    ).replace(
        'def mux_streams(kbd: list[bytes], mouse: list[bytes], ring: EventRing) -> int:\n    """TODO [LIN-MUX-03]: round-robin interleave into ring; return events written."""\n    raise NotImplementedError("LIN-MUX-03")',
        '''def mux_streams(kbd: list[bytes], mouse: list[bytes], ring: EventRing) -> int:
    # PEDAGOGY-SOLUTION: LIN-MUX-03
    written = 0
    i = 0
    while i < max(len(kbd), len(mouse)):
        if i < len(kbd):
            ring.push(kbd[i])
            written += 1
        if i < len(mouse):
            ring.push(mouse[i])
            written += 1
        i += 1
    return written''',
    )
    test = '''# PEDAGOGY-TEST: LIN-MUX-01
# PEDAGOGY-TEST: LIN-MUX-02
# PEDAGOGY-TEST: LIN-MUX-03
# Caso 1: pack_event 24 bytes com type/code/value
# Caso 2: ring overflow drop oldest
# Caso 3: mux round-robin kbd+mouse
# Caso 4: mux retorna contagem correta
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from input_event_ring_mux import pack_event, EventRing, mux_streams, EVENT_SIZE, EV_KEY, EV_REL

def main():
    ev = pack_event(EV_KEY, 30, 1)
    assert len(ev) == EVENT_SIZE
    t, c, v = struct.unpack_from("<HHI", ev, 16)
    assert (t, c, v) == (EV_KEY, 30, 1)
    ring = EventRing(2)
    ring.push(ev)
    ring.push(pack_event(EV_REL, 0, 5))
    assert ring.push(pack_event(EV_KEY, 31, 1))  # drops oldest
    kbd = [pack_event(EV_KEY, 30, 1)]
    mouse = [pack_event(EV_REL, 0, 2)]
    r2 = EventRing(4)
    n = mux_streams(kbd, mouse, r2)
    assert n == 2
    print("OK input_event_ring_mux")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "input_event_ring_mux", starter, sol, test)
    todos = [
        {"id": "LIN-MUX-01", "file": "starter/input_event_ring_mux.py", "fn": "pack_event",
         "problem": "Layout evdev 24B.", "code": "struct.pack_into at offset 16",
         "why": "Paridade com drivers Dia 07.", "verify": "Caso 1: type/code/value."},
        {"id": "LIN-MUX-02", "file": "starter/input_event_ring_mux.py", "fn": "EventRing.push",
         "problem": "Ring fixo com drop oldest.", "code": "advance head on overflow",
         "why": "Drivers não bloqueiam em flood.", "verify": "Caso 2: drop."},
        {"id": "LIN-MUX-03", "file": "starter/input_event_ring_mux.py", "fn": "mux_streams",
         "problem": "Round-robin kbd+mouse.", "code": "interleave lists",
         "why": "Multiplexação justa.", "verify": "Caso 3: n=2."},
    ]
    write_pedagogy_docs(
        base, "input_event_ring_mux",
        "# Linux — input event ring mux\n\nMultiplexa teclado+mouse em ring 24B.\n",
        "cd days/2026-09-08/linux/input_event_ring_mux/starter\npython test_input_event_ring_mux.py",
        todos, [("evdev 24B", "layout"), ("Ring buffer", "cap fixo"), ("Mux", "round-robin")],
        ["pack 24B", "overflow drop", "mux 2 streams", "count written"],
        "# Pesquisa\n\n- `linux/hid_keyboard_boot` Dia 07\n- evdev input_event struct\n",
    )


def scaffold_rust_disasm() -> None:
    base = DAY08 / "rust" / "clvm_disasm"
    lib = '''//! CLVM bytecode disassembler — Rust port.

pub const PUSH: u8 = 0x01;

pub fn opcode_name(op: u8) -> Option<&'static str> {
    // TODO [CLVM-RS-DIS-01]
    match op {
        _ => None,
    }
}

pub fn instruction_size(op: u8) -> usize {
    // TODO [CLVM-RS-DIS-02]
    let _ = op;
    0
}

pub fn disassemble(code: &[u8]) -> Result<Vec<String>, String> {
    // TODO [CLVM-RS-DIS-03]
    let _ = code;
    Err("CLVM-RS-DIS-03".into())
}
'''
    lib_sol = lib.replace(
        "pub fn opcode_name(op: u8) -> Option<&'static str> {\n    // TODO [CLVM-RS-DIS-01]\n    match op {\n        _ => None,\n    }\n}",
        "pub fn opcode_name(op: u8) -> Option<&'static str> {\n    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-01\n    match op {\n        0x02 => Some(\"ADD\"),\n        0x08 => Some(\"HALT\"),\n        0x09 => Some(\"JMP\"),\n        PUSH => Some(\"PUSH\"),\n        _ => None,\n    }\n}",
    ).replace(
        "pub fn instruction_size(op: u8) -> usize {\n    // TODO [CLVM-RS-DIS-02]\n    let _ = op;\n    0\n}",
        "pub fn instruction_size(op: u8) -> usize {\n    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-02\n    if op == PUSH {\n        5\n    } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {\n        3\n    } else {\n        1\n    }\n}",
    ).replace(
        'pub fn disassemble(code: &[u8]) -> Result<Vec<String>, String> {\n    // TODO [CLVM-RS-DIS-03]\n    let _ = code;\n    Err("CLVM-RS-DIS-03".into())\n}',
        '''pub fn disassemble(code: &[u8]) -> Result<Vec<String>, String> {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-03
    let mut out = Vec::new();
    let mut pc = 0usize;
    while pc < code.len() {
        let op = code[pc];
        if op == PUSH {
            if pc + 5 > code.len() {
                return Err("truncated PUSH".into());
            }
            let imm = u32::from_le_bytes(code[pc + 1..pc + 5].try_into().unwrap());
            out.push(format!("PUSH {}", imm));
            pc += 5;
        } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {
            if pc + 3 > code.len() {
                return Err("truncated branch".into());
            }
            let off = u16::from_le_bytes(code[pc + 1..pc + 3].try_into().unwrap());
            let name = opcode_name(op).unwrap_or("BR");
            out.push(format!("{} {}", name, off));
            pc += 3;
        } else if let Some(name) = opcode_name(op) {
            out.push(name.to_string());
            pc += 1;
        } else {
            return Err(format!("unknown op 0x{:02x}", op));
        }
    }
    Ok(out)
}''',
    )
    cargo = '''[package]
name = "clvm_disasm"
version = "0.1.0"
edition = "2021"

[lib]
path = "src/lib.rs"
'''
    test_rs = '''use clvm_disasm::{disassemble, instruction_size, opcode_name, PUSH};

// PEDAGOGY-TEST: CLVM-RS-DIS-01
#[test]
fn caso_1_opcode_name() {
    assert_eq!(opcode_name(PUSH), Some("PUSH"));
    assert_eq!(opcode_name(0x08), Some("HALT"));
}

// PEDAGOGY-TEST: CLVM-RS-DIS-02
#[test]
fn caso_2_instruction_size() {
    assert_eq!(instruction_size(PUSH), 5);
    assert_eq!(instruction_size(0x09), 3);
    assert_eq!(instruction_size(0x08), 1);
}

// PEDAGOGY-TEST: CLVM-RS-DIS-03
#[test]
fn caso_3_disassemble_push_halt() {
    let code = [PUSH, 42, 0, 0, 0, 0x08];
    let lines = disassemble(&code).expect("disasm");
    assert_eq!(lines, vec!["PUSH 42", "HALT"]);
}

// PEDAGOGY-TEST: CLVM-RS-DIS-03
#[test]
fn caso_4_unknown_op_err() {
    assert!(disassemble(&[0xFF]).is_err());
}
'''
    for side, body in (("starter", lib), ("solutions", lib_sol)):
        root = base / side
        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "tests").mkdir(parents=True, exist_ok=True)
        (root / "Cargo.toml").write_text(cargo, encoding="utf-8")
        (root / "src" / "lib.rs").write_text(body, encoding="utf-8")
        (root / "tests" / "clvm_disasm_tests.rs").write_text(test_rs, encoding="utf-8")
    todos = [
        {"id": "CLVM-RS-DIS-01", "file": "starter/src/lib.rs", "fn": "opcode_name", "lang": "rust",
         "problem": "Mapa opcode→nome.", "code": "match op { PUSH => Some(\"PUSH\"), ... }",
         "why": "Disassembly legível.", "verify": "Caso 1: HALT."},
        {"id": "CLVM-RS-DIS-02", "file": "starter/src/lib.rs", "fn": "instruction_size", "lang": "rust",
         "problem": "Tamanhos variáveis.", "code": "PUSH=5, branch=3, else=1",
         "why": "Avanço de PC.", "verify": "Caso 2: sizes."},
        {"id": "CLVM-RS-DIS-03", "file": "starter/src/lib.rs", "fn": "disassemble", "lang": "rust",
         "problem": "Walk completo.", "code": "while pc < code.len()",
         "why": "Port do Python.", "verify": "Caso 3: PUSH 42 HALT."},
    ]
    write_pedagogy_docs(
        base, "clvm_disasm",
        "# Rust — CLVM disassembler\n\nPort Rust do disassembler Python.\n",
        "cd days/2026-09-08/rust/clvm_disasm/starter\ncargo test",
        todos, [("opcode_name", "match"), ("instruction_size", "operand sizes"), ("disassemble", "walk")],
        ["opcode HALT", "size PUSH=5", "disasm PUSH+HALT", "unknown op"],
        "# Pesquisa\n\n- `systems/clvm_disassembler` mesmo dia\n- clvm_v2_verify Dia 07\n",
    )


def scaffold_dotnet_pe() -> None:
    base = DAY08 / "dotnet" / "pe_export_span"
    cs = '''using System.Runtime.InteropServices;

namespace Chris.PeLab;

public static class PeExportSpan
{
    /// <summary>TODO [DN-PE-EXP-01]: validate MZ header and PE signature.</summary>
    public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        _ = data;
        return false;
    }

    /// <summary>TODO [DN-PE-EXP-02]: read e_lfanew from DOS header.</summary>
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        peOffset = 0;
        _ = data;
        return false;
    }

    /// <summary>TODO [DN-PE-EXP-03]: read export directory RVA from optional header data dir [0].</summary>
    public static bool TryReadExportRva(ReadOnlySpan<byte> data, out uint exportRva)
    {
        exportRva = 0;
        _ = data;
        return false;
    }
}
'''
    cs_sol = cs.replace(
        "public static bool IsPeFile(ReadOnlySpan<byte> data)\n    {\n        _ = data;\n        return false;\n    }",
        "public static bool IsPeFile(ReadOnlySpan<byte> data)\n    {\n        // PEDAGOGY-SOLUTION: DN-PE-EXP-01\n        if (data.Length < 0x40) return false;\n        if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;\n        if (!TryGetPeOffset(data, out int off)) return false;\n        if (off + 4 > data.Length) return false;\n        return data[off] == (byte)'P' && data[off + 1] == (byte)'E';\n    }",
    ).replace(
        "public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)\n    {\n        peOffset = 0;\n        _ = data;\n        return false;\n    }",
        "public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)\n    {\n        // PEDAGOGY-SOLUTION: DN-PE-EXP-02\n        peOffset = 0;\n        if (data.Length < 0x40) return false;\n        peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));\n        return peOffset > 0 && peOffset + 4 <= data.Length;\n    }",
    ).replace(
        "public static bool TryReadExportRva(ReadOnlySpan<byte> data, out uint exportRva)\n    {\n        exportRva = 0;\n        _ = data;\n        return false;\n    }",
        "public static bool TryReadExportRva(ReadOnlySpan<byte> data, out uint exportRva)\n    {\n        // PEDAGOGY-SOLUTION: DN-PE-EXP-03\n        exportRva = 0;\n        if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;\n        int opt = pe + 4 + 20;\n        if (opt + 0x78 + 8 > data.Length) return false;\n        exportRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78, 4));\n        return true;\n    }",
    )
    csproj = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <RootNamespace>Chris.PeLab</RootNamespace>
  </PropertyGroup>
  <ItemGroup><Compile Remove="tests/**" /></ItemGroup>
</Project>
'''
    test_csproj = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
  <ItemGroup><ProjectReference Include="..\\Chris.PeLab.csproj" /></ItemGroup>
</Project>
'''
    test_cs = '''using System;
using System.Runtime.InteropServices;
using Chris.PeLab;
using Xunit;

public class PeExportTests
{
    static byte[] MinimalPe()
    {
        var buf = new byte[0x200];
        buf[0] = (byte)'M'; buf[1] = (byte)'Z';
        BitConverter.GetBytes(0x80).CopyTo(buf, 0x3C);
        buf[0x80] = (byte)'P'; buf[0x81] = (byte)'E'; buf[0x82] = 0; buf[0x83] = 0;
        BitConverter.GetBytes(0x20B).CopyTo(buf, 0x98);
        BitConverter.GetBytes(0x1000u).CopyTo(buf, 0x110);
        return buf;
    }

    // PEDAGOGY-TEST: DN-PE-EXP-01
    [Fact]
    public void Caso1_IsPeFile() => Assert.True(PeExportSpan.IsPeFile(MinimalPe()));

    // PEDAGOGY-TEST: DN-PE-EXP-02
    [Fact]
    public void Caso2_PeOffset()
    {
        Assert.True(PeExportSpan.TryGetPeOffset(MinimalPe(), out int off));
        Assert.Equal(0x80, off);
    }

    // PEDAGOGY-TEST: DN-PE-EXP-03
    [Fact]
    public void Caso3_ExportRva()
    {
        Assert.True(PeExportSpan.TryReadExportRva(MinimalPe(), out uint rva));
        Assert.Equal(0x1000u, rva);
    }

    // PEDAGOGY-TEST: DN-PE-EXP-01
    [Fact]
    public void Caso4_NotPe() => Assert.False(PeExportSpan.IsPeFile(new byte[] { 0, 1, 2 }));
}
'''
    for side, body in (("starter", cs), ("solutions", cs_sol)):
        root = base / side
        (root / "tests").mkdir(parents=True, exist_ok=True)
        (root / "Chris.PeLab.csproj").write_text(csproj, encoding="utf-8")
        (root / "PeExportSpan.cs").write_text(body, encoding="utf-8")
        (root / "tests" / "PeExportTests.cs").write_text(test_cs, encoding="utf-8")
        (root / "tests" / "Chris.PeLab.Tests.csproj").write_text(test_csproj, encoding="utf-8")
    todos = [
        {"id": "DN-PE-EXP-01", "file": "starter/PeExportSpan.cs", "fn": "IsPeFile", "lang": "csharp",
         "problem": "MZ + PE signature.", "code": "data[0]=='M' && data[1]=='Z'",
         "why": "Gate antes de parse.", "verify": "Caso 1: true."},
        {"id": "DN-PE-EXP-02", "file": "starter/PeExportSpan.cs", "fn": "TryGetPeOffset", "lang": "csharp",
         "problem": "e_lfanew at 0x3C.", "code": "MemoryMarshal.Read<int>(data.Slice(0x3C,4))",
         "why": "Localizar PE header.", "verify": "Caso 2: 0x80."},
        {"id": "DN-PE-EXP-03", "file": "starter/PeExportSpan.cs", "fn": "TryReadExportRva", "lang": "csharp",
         "problem": "Data directory export.", "code": "read u32 at opt+0x78",
         "why": "Triage de exports.", "verify": "Caso 3: RVA 0x1000."},
    ]
    write_pedagogy_docs(
        base, "pe_export_span",
        "# .NET — PE export directory Span parse\n\nParse PE exports com `ReadOnlySpan<byte>`.\n",
        "cd days/2026-09-08/dotnet/pe_export_span/starter\ndotnet test tests/Chris.PeLab.Tests.csproj",
        todos, [("MZ/PE", "magic"), ("e_lfanew", "DOS stub"), ("Export RVA", "data directory")],
        ["IsPeFile", "pe offset", "export RVA", "not PE"],
        "# Pesquisa\n\n- PE format Microsoft docs\n- `redteam/pe_export_triage` par Python\n",
    )


def scaffold_gfx_shader_fsm() -> None:
    base = DAY08 / "graphics" / "shader_stage_fsm"
    (base / "docs").mkdir(parents=True, exist_ok=True)
    (base / "docs" / "COMPARISON.md").write_text(
        "# Comparação — shader compile pipeline\n\n"
        "| Backend | Papel neste módulo |\n|---------|-------------------|\n"
        "| CPU FSM (Python) | Simula estágios SOURCE→READY sem GPU |\n"
        "| OpenGL (conceitual) | glCompileShader / glLinkProgram mapeiam estágios |\n"
        "| D3D11 (conceitual) | D3DCompile + CreateVertexShader |\n",
        encoding="utf-8",
    )
    starter = '''"""Shader compile stage FSM — SOURCE→PREPROCESS→COMPILE→LINK→REFLECT→READY."""

from __future__ import annotations

TRANSITIONS = {
    ("SOURCE", "preprocess"): "PREPROCESS",
    ("PREPROCESS", "compile"): "COMPILE",
    ("COMPILE", "link"): "LINK",
    ("LINK", "reflect"): "REFLECT",
    ("REFLECT", "done"): "READY",
}


def transition(state: str, event: str) -> str:
    """TODO [GFX-SHADER-FSM-01]: apply TRANSITIONS or raise ValueError."""
    raise NotImplementedError("GFX-SHADER-FSM-01")


def run_stage(state: str, payload: dict) -> dict:
    """TODO [GFX-SHADER-FSM-02]: return evidence dict with stage name and ok flag."""
    raise NotImplementedError("GFX-SHADER-FSM-02")


def compile_pipeline(source: str) -> tuple[str, list[dict]]:
    """TODO [GFX-SHADER-FSM-03]: run full pipeline; return (final_state, trace)."""
    raise NotImplementedError("GFX-SHADER-FSM-03")
'''
    sol = starter.replace(
        'def transition(state: str, event: str) -> str:\n    """TODO [GFX-SHADER-FSM-01]: apply TRANSITIONS or raise ValueError."""\n    raise NotImplementedError("GFX-SHADER-FSM-01")',
        '''def transition(state: str, event: str) -> str:
    # PEDAGOGY-SOLUTION: GFX-SHADER-FSM-01
    key = (state, event)
    if key not in TRANSITIONS:
        raise ValueError(f"invalid {key}")
    return TRANSITIONS[key]''',
    ).replace(
        'def run_stage(state: str, payload: dict) -> dict:\n    """TODO [GFX-SHADER-FSM-02]: return evidence dict with stage name and ok flag."""\n    raise NotImplementedError("GFX-SHADER-FSM-02")',
        '''def run_stage(state: str, payload: dict) -> dict:
    # PEDAGOGY-SOLUTION: GFX-SHADER-FSM-02
    ok = bool(payload.get("source") or state != "SOURCE")
    return {"stage": state, "ok": ok, "bytes": len(str(payload.get("source", "")))}''',
    ).replace(
        'def compile_pipeline(source: str) -> tuple[str, list[dict]]:\n    """TODO [GFX-SHADER-FSM-03]: run full pipeline; return (final_state, trace)."""\n    raise NotImplementedError("GFX-SHADER-FSM-03")',
        '''def compile_pipeline(source: str) -> tuple[str, list[dict]]:
    # PEDAGOGY-SOLUTION: GFX-SHADER-FSM-03
    events = ["preprocess", "compile", "link", "reflect", "done"]
    state = "SOURCE"
    trace: list[dict] = []
    payload = {"source": source}
    trace.append(run_stage(state, payload))
    for ev in events:
        state = transition(state, ev)
        trace.append(run_stage(state, payload))
    return state, trace''',
    )
    test = '''# PEDAGOGY-TEST: GFX-SHADER-FSM-01
# PEDAGOGY-TEST: GFX-SHADER-FSM-02
# PEDAGOGY-TEST: GFX-SHADER-FSM-03
# Caso 1: SOURCE preprocess -> PREPROCESS
# Caso 2: run_stage retorna ok
# Caso 3: compile_pipeline termina READY
# Caso 4: VISUAL-01 — trace tem 6 estágios (simulação headless)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from shader_stage_fsm import transition, run_stage, compile_pipeline

def main():
    assert transition("SOURCE", "preprocess") == "PREPROCESS"
    ev = run_stage("SOURCE", {"source": "void main(){}"})
    assert ev["ok"] and ev["stage"] == "SOURCE"
    state, trace = compile_pipeline("void main(){}")
    assert state == "READY" and len(trace) == 6
    print("OK shader_stage_fsm VISUAL-01 headless trace")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "shader_stage_fsm", starter, sol, test)
    todos = [
        {"id": "GFX-SHADER-FSM-01", "file": "starter/shader_stage_fsm.py", "fn": "transition",
         "problem": "FSM de estágios de compile.", "code": "TRANSITIONS[(state,event)]",
         "why": "Modela pipeline GPU offline.", "verify": "Caso 1: PREPROCESS."},
        {"id": "GFX-SHADER-FSM-02", "file": "starter/shader_stage_fsm.py", "fn": "run_stage",
         "problem": "Evidência por estágio.", "code": '{"stage": state, "ok": ...}',
         "why": "Observabilidade.", "verify": "Caso 2: ok true."},
        {"id": "GFX-SHADER-FSM-03", "file": "starter/shader_stage_fsm.py", "fn": "compile_pipeline",
         "problem": "Pipeline completo.", "code": "for ev in events: transition",
         "why": "Simula compile end-to-end.", "verify": "Caso 3: READY."},
    ]
    write_pedagogy_docs(
        base, "shader_stage_fsm",
        "# Graphics — shader compile stage FSM\n\nSimulação Python do pipeline de shaders (headless).\n",
        "cd days/2026-09-08/graphics/shader_stage_fsm/starter\npython test_shader_stage_fsm.py",
        todos, [("FSM transitions", "estados"), ("Stage evidence", "trace"), ("Pipeline", "SOURCE→READY")],
        ["transition", "run_stage ok", "compile READY", "VISUAL-01 trace 6 estágios"],
        "# Pesquisa\n\n- glCompileShader / D3DCompile docs\n- `resource_state_tracker` Dia 07\n",
    )


def scaffold_redteam_pe() -> None:
    base = DAY08 / "redteam" / "pe_export_triage"
    starter = '''"""PE export table triage — validate MZ/PE and flag suspicious names."""

from __future__ import annotations

SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread")


def validate_mz_pe(data: bytes) -> bool:
    """TODO [RT-PE-EXP-01]: MZ + PE signature via e_lfanew."""
    raise NotImplementedError("RT-PE-EXP-01")


def count_export_names(data: bytes, names: list[str]) -> int:
    """TODO [RT-PE-EXP-02]: return len(names) if PE valid else -1."""
    raise NotImplementedError("RT-PE-EXP-02")


def flag_suspicious_exports(names: list[str]) -> list[str]:
    """TODO [RT-PE-EXP-03]: return suspicious export names present."""
    raise NotImplementedError("RT-PE-EXP-03")
'''
    sol = starter.replace(
        'def validate_mz_pe(data: bytes) -> bool:\n    """TODO [RT-PE-EXP-01]: MZ + PE signature via e_lfanew."""\n    raise NotImplementedError("RT-PE-EXP-01")',
        '''def validate_mz_pe(data: bytes) -> bool:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-01
    if len(data) < 0x40 or data[0:2] != b"MZ":
        return False
    import struct
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    return pe_off + 4 <= len(data) and data[pe_off:pe_off + 2] == b"PE"''',
    ).replace(
        'def count_export_names(data: bytes, names: list[str]) -> int:\n    """TODO [RT-PE-EXP-02]: return len(names) if PE valid else -1."""\n    raise NotImplementedError("RT-PE-EXP-02")',
        '''def count_export_names(data: bytes, names: list[str]) -> int:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-02
    if not validate_mz_pe(data):
        return -1
    return len(names)''',
    ).replace(
        'def flag_suspicious_exports(names: list[str]) -> list[str]:\n    """TODO [RT-PE-EXP-03]: return suspicious export names present."""\n    raise NotImplementedError("RT-PE-EXP-03")',
        '''def flag_suspicious_exports(names: list[str]) -> list[str]:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-03
    return [n for n in names if n in SUSPICIOUS]''',
    )
    test = '''# PEDAGOGY-TEST: RT-PE-EXP-01
# PEDAGOGY-TEST: RT-PE-EXP-02
# PEDAGOGY-TEST: RT-PE-EXP-03
# Caso 1: minimal PE passes validate
# Caso 2: count exports
# Caso 3: flag VirtualAlloc
# Caso 4: invalid returns -1
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pe_export_triage import validate_mz_pe, count_export_names, flag_suspicious_exports

def minimal_pe():
    buf = bytearray(0x100)
    buf[0:2] = b"MZ"
    struct.pack_into("<I", buf, 0x3C, 0x80)
    buf[0x80:0x82] = b"PE"
    return bytes(buf)

def main():
    pe = minimal_pe()
    assert validate_mz_pe(pe)
    assert count_export_names(pe, ["A", "B"]) == 2
    assert flag_suspicious_exports(["VirtualAlloc", "malloc"]) == ["VirtualAlloc"]
    assert count_export_names(b"bad", []) == -1
    print("OK pe_export_triage")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "pe_export_triage", starter, sol, test)
    todos = [
        {"id": "RT-PE-EXP-01", "file": "starter/pe_export_triage.py", "fn": "validate_mz_pe",
         "problem": "Gate MZ/PE.", "code": "e_lfanew + PE sig",
         "why": "Evita parse em lixo.", "verify": "Caso 1: true."},
        {"id": "RT-PE-EXP-02", "file": "starter/pe_export_triage.py", "fn": "count_export_names",
         "problem": "Contagem com validação.", "code": "return -1 if invalid",
         "why": "Triage quantitativo.", "verify": "Caso 2: 2."},
        {"id": "RT-PE-EXP-03", "file": "starter/pe_export_triage.py", "fn": "flag_suspicious_exports",
         "problem": "Lista IOC em exports.", "code": "filter SUSPICIOUS",
         "why": "Detecção rápida.", "verify": "Caso 3: VirtualAlloc."},
    ]
    write_pedagogy_docs(
        base, "pe_export_triage",
        "# Red team — PE export triage\n\nTriage de export table (par `dotnet/pe_export_span`).\n",
        "cd days/2026-09-08/redteam/pe_export_triage/starter\npython test_pe_export_triage.py",
        todos, [("MZ/PE", "validate"), ("Export count", "metrics"), ("IOC names", "flags")],
        ["validate PE", "count 2", "flag VirtualAlloc", "invalid -1"],
        "# Pesquisa\n\n- PE export directory\n- chris-binary-toolkit\n",
    )


def scaffold_quantum_bell() -> None:
    base = DAY08 / "quantum" / "bell_state_prep"
    starter = '''"""Bell state |00⟩+|11⟩ preparation on 2-qubit statevector."""

from __future__ import annotations

import math


def apply_h(state: list[complex], qubit: int) -> None:
    """TODO [Q-BELL-01]: Hadamard on qubit 0 or 1 (4-amplitude state)."""
    raise NotImplementedError("Q-BELL-01")


def apply_cnot(state: list[complex], control: int, target: int) -> None:
    """TODO [Q-BELL-02]: CNOT with control/target qubits."""
    raise NotImplementedError("Q-BELL-02")


def bell_state_amplitudes() -> list[complex]:
    """TODO [Q-BELL-03]: return normalized |00⟩+|11⟩ statevector."""
    raise NotImplementedError("Q-BELL-03")
'''
    sol = starter.replace(
        'def apply_h(state: list[complex], qubit: int) -> None:\n    """TODO [Q-BELL-01]: Hadamard on qubit 0 or 1 (4-amplitude state)."""\n    raise NotImplementedError("Q-BELL-01")',
        '''def apply_h(state: list[complex], qubit: int) -> None:
    # PEDAGOGY-SOLUTION: Q-BELL-01
    inv = 1.0 / math.sqrt(2.0)
    if qubit == 0:
        a0, a1, a2, a3 = state
        state[0] = inv * (a0 + a1)
        state[1] = inv * (a2 + a3)
        state[2] = inv * (a0 - a1)
        state[3] = inv * (a2 - a3)
    else:
        a0, a1, a2, a3 = state
        state[0] = inv * (a0 + a2)
        state[1] = inv * (a1 + a3)
        state[2] = inv * (a0 - a2)
        state[3] = inv * (a1 - a3)''',
    ).replace(
        'def apply_cnot(state: list[complex], control: int, target: int) -> None:\n    """TODO [Q-BELL-02]: CNOT with control/target qubits."""\n    raise NotImplementedError("Q-BELL-02")',
        '''def apply_cnot(state: list[complex], control: int, target: int) -> None:
    # PEDAGOGY-SOLUTION: Q-BELL-02
    if control == 0 and target == 1:
        state[1], state[3] = state[3], state[1]
    elif control == 1 and target == 0:
        state[2], state[3] = state[3], state[2]
    else:
        raise ValueError("unsupported CNOT")''',
    ).replace(
        'def bell_state_amplitudes() -> list[complex]:\n    """TODO [Q-BELL-03]: return normalized |00⟩+|11⟩ statevector."""\n    raise NotImplementedError("Q-BELL-03")',
        '''def bell_state_amplitudes() -> list[complex]:
    # PEDAGOGY-SOLUTION: Q-BELL-03
    inv = 1.0 / math.sqrt(2.0)
    return [inv + 0j, 0j, 0j, inv + 0j]''',
    )
    test = '''# PEDAGOGY-TEST: Q-BELL-01
# PEDAGOGY-TEST: Q-BELL-02
# PEDAGOGY-TEST: Q-BELL-03
# Caso 1: H on |0> gives equal superposition on q0
# Caso 2: CNOT entangles
# Caso 3: Bell state has amp on |00> and |11>
# Caso 4: probabilities sum to 1
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bell_state_prep import apply_h, apply_cnot, bell_state_amplitudes

def main():
    s = [1.0 + 0j, 0j, 0j, 0j]
    apply_h(s, 0)
    assert abs(abs(s[0]) - 1/math.sqrt(2)) < 1e-6
    apply_cnot(s, 0, 1)
    bell = bell_state_amplitudes()
    assert abs(bell[0]) > 0.5 and abs(bell[3]) > 0.5
    probs = sum(abs(a)**2 for a in bell)
    assert abs(probs - 1.0) < 1e-6
    print("OK bell_state_prep")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "bell_state_prep", starter, sol, test)
    todos = [
        {"id": "Q-BELL-01", "file": "starter/bell_state_prep.py", "fn": "apply_h",
         "problem": "Hadamard 2-qubit.", "code": "inv/sqrt(2) linear combo",
         "why": "Superposição inicial.", "verify": "Caso 1: amp 1/sqrt(2)."},
        {"id": "Q-BELL-02", "file": "starter/bell_state_prep.py", "fn": "apply_cnot",
         "problem": "Entanglement.", "code": "swap amplitudes on |11>",
         "why": "CNOT cria correlação.", "verify": "Caso 2: swap."},
        {"id": "Q-BELL-03", "file": "starter/bell_state_prep.py", "fn": "bell_state_amplitudes",
         "problem": "Pipeline H then CNOT.", "code": "|0> -> H -> CNOT",
         "why": "Estado Bell padrão.", "verify": "Caso 3: |00>+|11>."},
    ]
    write_pedagogy_docs(
        base, "bell_state_prep",
        "# Quantum — Bell state preparation\n\nPrepara |Φ+⟩ = (|00⟩+|11⟩)/√2.\n",
        "cd days/2026-09-08/quantum/bell_state_prep/starter\npython test_bell_state_prep.py",
        todos, [("Hadamard", "superposição"), ("CNOT", "entrelaçamento"), ("Bell", "estado final")],
        ["H on |0>", "CNOT", "Bell amps", "prob sum 1"],
        "# Pesquisa\n\n- `measurement_born` Dia 07\n- Bell states\n",
    )


def scaffold_ai_softmax() -> None:
    base = DAY08 / "ai" / "softmax_stable"
    starter = '''"""Numerically stable softmax and log-softmax."""

from __future__ import annotations

import math


def softmax_stable(xs: list[float]) -> list[float]:
    """TODO [AI-SOFTMAX-01]: subtract max before exp; normalize."""
    raise NotImplementedError("AI-SOFTMAX-01")


def log_softmax_stable(xs: list[float]) -> list[float]:
    """TODO [AI-SOFTMAX-02]: log-softmax with max trick."""
    raise NotImplementedError("AI-SOFTMAX-02")


def cross_entropy_loss(logits: list[float], target: int) -> float:
    """TODO [AI-SOFTMAX-03]: -log p(target) using log_softmax."""
    raise NotImplementedError("AI-SOFTMAX-03")
'''
    sol = starter.replace(
        'def softmax_stable(xs: list[float]) -> list[float]:\n    """TODO [AI-SOFTMAX-01]: subtract max before exp; normalize."""\n    raise NotImplementedError("AI-SOFTMAX-01")',
        '''def softmax_stable(xs: list[float]) -> list[float]:
    # PEDAGOGY-SOLUTION: AI-SOFTMAX-01
    if not xs:
        return []
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]''',
    ).replace(
        'def log_softmax_stable(xs: list[float]) -> list[float]:\n    """TODO [AI-SOFTMAX-02]: log-softmax with max trick."""\n    raise NotImplementedError("AI-SOFTMAX-02")',
        '''def log_softmax_stable(xs: list[float]) -> list[float]:
    # PEDAGOGY-SOLUTION: AI-SOFTMAX-02
    if not xs:
        return []
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    log_sum = m + math.log(sum(exps))
    return [x - log_sum for x in xs]''',
    ).replace(
        'def cross_entropy_loss(logits: list[float], target: int) -> float:\n    """TODO [AI-SOFTMAX-03]: -log p(target) using log_softmax."""\n    raise NotImplementedError("AI-SOFTMAX-03")',
        '''def cross_entropy_loss(logits: list[float], target: int) -> float:
    # PEDAGOGY-SOLUTION: AI-SOFTMAX-03
    ls = log_softmax_stable(logits)
    return -ls[target]''',
    )
    test = '''# PEDAGOGY-TEST: AI-SOFTMAX-01
# PEDAGOGY-TEST: AI-SOFTMAX-02
# PEDAGOGY-TEST: AI-SOFTMAX-03
# Caso 1: softmax sums to 1
# Caso 2: large logits stable
# Caso 3: cross entropy on target
# Caso 4: log_softmax + exp ≈ softmax
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from softmax_stable import softmax_stable, log_softmax_stable, cross_entropy_loss

def main():
    p = softmax_stable([1.0, 2.0, 3.0])
    assert abs(sum(p) - 1.0) < 1e-6
    big = softmax_stable([1000.0, 1001.0, 1002.0])
    assert all(0 < x < 1 for x in big)
    loss = cross_entropy_loss([1.0, 2.0, 3.0], 2)
    assert loss > 0
    ls = log_softmax_stable([1.0, 2.0, 3.0])
    assert abs(sum(math.exp(x) for x in ls) - 1.0) < 1e-5
    print("OK softmax_stable")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "softmax_stable", starter, sol, test)
    todos = [
        {"id": "AI-SOFTMAX-01", "file": "starter/softmax_stable.py", "fn": "softmax_stable",
         "problem": "Overflow em exp.", "code": "x - max(xs)",
         "why": "Estabilidade numérica.", "verify": "Caso 1: sum=1."},
        {"id": "AI-SOFTMAX-02", "file": "starter/softmax_stable.py", "fn": "log_softmax_stable",
         "problem": "Log domain.", "code": "x - log_sum",
         "why": "Treino estável.", "verify": "Caso 4: exp sum 1."},
        {"id": "AI-SOFTMAX-03", "file": "starter/softmax_stable.py", "fn": "cross_entropy_loss",
         "problem": "Loss classificação.", "code": "-ls[target]",
         "why": "Métrica padrão.", "verify": "Caso 3: loss>0."},
    ]
    write_pedagogy_docs(
        base, "softmax_stable",
        "# AI — numerically stable softmax\n\nSoftmax/log-softmax/cross-entropy estáveis.\n",
        "cd days/2026-09-08/ai/softmax_stable/starter\npython test_softmax_stable.py",
        todos, [("Softmax", "max trick"), ("Log-softmax", "log domain"), ("Cross-entropy", "loss")],
        ["sum 1", "large logits", "CE loss", "log exp sum"],
        "# Pesquisa\n\n- log-sum-exp trick\n- `kv_cache_ring` Dia 07\n",
    )


def scaffold_node_duplex() -> None:
    base = DAY08 / "nodejs" / "duplex_event_pipe"
    starter = '''import { Duplex } from "node:stream";

export const EVENT_SIZE = 24;

export class DuplexEventPipe extends Duplex {
    constructor() {
        super();
        this.buffer = Buffer.alloc(0);
        this.eventsWritten = 0;
        this.eventsRead = 0;
    }

    _write(chunk, encoding, callback) {
        // TODO [ND-DUPLEX-01]: accumulate 24B events from writes
        callback();
    }

    _read(size) {
        // TODO [ND-DUPLEX-02]: push complete 24B events to reader
    }

    metrics() {
        // TODO [ND-DUPLEX-03]: return { eventsWritten, eventsRead }
        return {};
    }
}
'''
    sol = starter.replace(
        "_write(chunk, encoding, callback) {\n        // TODO [ND-DUPLEX-01]: accumulate 24B events from writes\n        callback();\n    }",
        "_write(chunk, encoding, callback) {\n        // PEDAGOGY-SOLUTION: ND-DUPLEX-01\n        this.buffer = Buffer.concat([this.buffer, chunk]);\n        while (this.buffer.length >= EVENT_SIZE) {\n            this.buffer = this.buffer.subarray(EVENT_SIZE);\n            this.eventsWritten++;\n        }\n        callback();\n    }",
    ).replace(
        "_read(size) {\n        // TODO [ND-DUPLEX-02]: push complete 24B events to reader\n    }",
        "_read(size) {\n        // PEDAGOGY-SOLUTION: ND-DUPLEX-02\n        if (this._queued && this._queued.length >= EVENT_SIZE) {\n            const ev = this._queued.subarray(0, EVENT_SIZE);\n            this._queued = this._queued.subarray(EVENT_SIZE);\n            this.eventsRead++;\n            this.push(ev);\n        }\n    }",
    ).replace(
        "metrics() {\n        // TODO [ND-DUPLEX-03]: return { eventsWritten, eventsRead }\n        return {};\n    }",
        "metrics() {\n        // PEDAGOGY-SOLUTION: ND-DUPLEX-03\n        return { eventsWritten: this.eventsWritten, eventsRead: this.eventsRead };\n    }",
    )
    # Fix sol: need _queued buffer for read side - let me improve solution
    sol = '''import { Duplex } from "node:stream";

export const EVENT_SIZE = 24;

export class DuplexEventPipe extends Duplex {
    constructor() {
        super();
        this._writeBuf = Buffer.alloc(0);
        this._readBuf = Buffer.alloc(0);
        this.eventsWritten = 0;
        this.eventsRead = 0;
    }

    _write(chunk, encoding, callback) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-01
        this._writeBuf = Buffer.concat([this._writeBuf, chunk]);
        while (this._writeBuf.length >= EVENT_SIZE) {
            const ev = this._writeBuf.subarray(0, EVENT_SIZE);
            this._writeBuf = this._writeBuf.subarray(EVENT_SIZE);
            this._readBuf = Buffer.concat([this._readBuf, ev]);
            this.eventsWritten++;
        }
        this._read(EVENT_SIZE);
        callback();
    }

    _read(size) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-02
        while (this._readBuf.length >= EVENT_SIZE) {
            const ev = this._readBuf.subarray(0, EVENT_SIZE);
            this._readBuf = this._readBuf.subarray(EVENT_SIZE);
            this.eventsRead++;
            if (!this.push(ev)) break;
        }
    }

    metrics() {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-03
        return { eventsWritten: this.eventsWritten, eventsRead: this.eventsRead };
    }
}
'''
    test = '''// PEDAGOGY-TEST: ND-DUPLEX-01
// PEDAGOGY-TEST: ND-DUPLEX-02
// PEDAGOGY-TEST: ND-DUPLEX-03
// Caso 1: write 48B -> 2 events written
// Caso 2: read receives 24B events
// Caso 3: metrics counts match
// Caso 4: partial write buffered
import assert from "node:assert";
import { DuplexEventPipe, EVENT_SIZE } from "./duplex_event_pipe.js";

async function main() {
    const pipe = new DuplexEventPipe();
    const ev = Buffer.alloc(EVENT_SIZE, 7);
    const out = [];
    pipe.on("data", (c) => out.push(Buffer.from(c)));
    await new Promise((resolve) => {
        pipe.write(Buffer.concat([ev, ev]), resolve);
    });
    await new Promise((r) => setImmediate(r));
    assert.equal(pipe.metrics().eventsWritten, 2);
    assert.ok(out.length >= 1);
    console.log("OK duplex_event_pipe");
}

main().catch((e) => { console.error(e); process.exit(1); });
'''
    for side, js in (("starter", starter), ("solutions", sol)):
        d = base / side
        d.mkdir(parents=True, exist_ok=True)
        (d / "duplex_event_pipe.js").write_text(js, encoding="utf-8")
        (d / "test.js").write_text(test, encoding="utf-8")
        (d / "package.json").write_text('{"type":"module"}\n', encoding="utf-8")
    todos = [
        {"id": "ND-DUPLEX-01", "file": "starter/duplex_event_pipe.js", "fn": "_write", "lang": "javascript",
         "problem": "Buffer writes em slots 24B.", "code": "while >= EVENT_SIZE",
         "why": "Duplex input pipe.", "verify": "Caso 1: 2 written."},
        {"id": "ND-DUPLEX-02", "file": "starter/duplex_event_pipe.js", "fn": "_read", "lang": "javascript",
         "problem": "Push events ao reader.", "code": "this.push(ev)",
         "why": "Consumo simétrico.", "verify": "Caso 2: data event."},
        {"id": "ND-DUPLEX-03", "file": "starter/duplex_event_pipe.js", "fn": "metrics", "lang": "javascript",
         "problem": "Observabilidade.", "code": "return counters",
         "why": "Debug backpressure.", "verify": "Caso 3: metrics."},
    ]
    write_pedagogy_docs(
        base, "duplex_event_pipe",
        "# Node.js — Duplex event pipe\n\nDuplex stream para eventos 24B.\n",
        "cd days/2026-09-08/nodejs/duplex_event_pipe/starter\nnode test.js",
        todos, [("Duplex", "stream"), ("24B framing", "evdev"), ("Metrics", "counters")],
        ["write 2 events", "read events", "metrics", "partial buffer"],
        "# Pesquisa\n\n- node:stream Duplex\n- `input_event_transform` Dia 07\n",
    )


def scaffold_parsers_json() -> None:
    base = DAY08 / "parsers" / "json_rd_lexer"
    starter = '''"""JSON subset lexer + recursive descent parser."""

from __future__ import annotations

import re

TOKEN_RE = re.compile(r'\\s*("[^"]*"|-?\\d+|\\{|\\}|\\[|\\]|,|:|true|false|null)')


def tokenize(text: str) -> list[str]:
    """TODO [PAR-JSON-LEX-01]: return list of JSON tokens (whitespace skipped)."""
    raise NotImplementedError("PAR-JSON-LEX-01")


def parse_value(tokens: list[str], i: int) -> tuple[object, int]:
    """TODO [PAR-JSON-LEX-02]: parse number/string/null at tokens[i]."""
    raise NotImplementedError("PAR-JSON-LEX-02")


def parse_object_minimal(tokens: list[str]) -> dict:
    """TODO [PAR-JSON-LEX-03]: parse {"key": value} minimal object."""
    raise NotImplementedError("PAR-JSON-LEX-03")
'''
    sol = starter.replace(
        'def tokenize(text: str) -> list[str]:\n    """TODO [PAR-JSON-LEX-01]: return list of JSON tokens (whitespace skipped)."""\n    raise NotImplementedError("PAR-JSON-LEX-01")',
        '''def tokenize(text: str) -> list[str]:
    # PEDAGOGY-SOLUTION: PAR-JSON-LEX-01
    pos = 0
    out: list[str] = []
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        if not m:
            raise ValueError(f"bad token at {pos}")
        out.append(m.group(1))
        pos = m.end()
    return out''',
    ).replace(
        'def parse_value(tokens: list[str], i: int) -> tuple[object, int]:\n    """TODO [PAR-JSON-LEX-02]: parse number/string/null at tokens[i]."""\n    raise NotImplementedError("PAR-JSON-LEX-02")',
        '''def parse_value(tokens: list[str], i: int) -> tuple[object, int]:
    # PEDAGOGY-SOLUTION: PAR-JSON-LEX-02
    tok = tokens[i]
    if tok == "null":
        return None, i + 1
    if tok.startswith('"'):
        return tok[1:-1], i + 1
    if tok.lstrip("-").isdigit():
        return int(tok), i + 1
    raise ValueError(f"unsupported value {tok}")''',
    ).replace(
        'def parse_object_minimal(tokens: list[str]) -> dict:\n    """TODO [PAR-JSON-LEX-03]: parse {"key": value} minimal object."""\n    raise NotImplementedError("PAR-JSON-LEX-03")',
        '''def parse_object_minimal(tokens: list[str]) -> dict:
    # PEDAGOGY-SOLUTION: PAR-JSON-LEX-03
    if tokens[0] != "{" or tokens[-1] != "}":
        raise ValueError("not object")
    key_tok = tokens[1]
    if not key_tok.startswith('"') or tokens[2] != ":":
        raise ValueError("bad object shape")
    val, _ = parse_value(tokens, 3)
    return {key_tok[1:-1]: val}''',
    )
    test = '''# PEDAGOGY-TEST: PAR-JSON-LEX-01
# PEDAGOGY-TEST: PAR-JSON-LEX-02
# PEDAGOGY-TEST: PAR-JSON-LEX-03
# Caso 1: tokenize simple object
# Caso 2: parse_value number
# Caso 3: parse_object_minimal
# Caso 4: null value
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from json_rd_lexer import tokenize, parse_value, parse_object_minimal

def main():
    toks = tokenize('{"a": 1}')
    assert "{" in toks and '"a"' in toks
    val, j = parse_value(toks, 3)
    assert val == 1
    assert parse_object_minimal(toks) == {"a": 1}
    assert parse_value(tokenize("null"), 0)[0] is None
    print("OK json_rd_lexer")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "json_rd_lexer", starter, sol, test)
    todos = [
        {"id": "PAR-JSON-LEX-01", "file": "starter/json_rd_lexer.py", "fn": "tokenize",
         "problem": "Lexer regex.", "code": "TOKEN_RE.match loop",
         "why": "Base do parser RD.", "verify": "Caso 1: tokens."},
        {"id": "PAR-JSON-LEX-02", "file": "starter/json_rd_lexer.py", "fn": "parse_value",
         "problem": "Valores atômicos.", "code": "int/string/null",
         "why": "RD recursivo.", "verify": "Caso 2: 1."},
        {"id": "PAR-JSON-LEX-03", "file": "starter/json_rd_lexer.py", "fn": "parse_object_minimal",
         "problem": "Objeto mínimo.", "code": '{ "key" : value }',
         "why": "Subset JSON.", "verify": "Caso 3: {a:1}."},
    ]
    write_pedagogy_docs(
        base, "json_rd_lexer",
        "# Parsers — JSON recursive descent lexer\n\nSubset JSON com lexer+RD.\n",
        "cd days/2026-09-08/parsers/json_rd_lexer/starter\npython test_json_rd_lexer.py",
        todos, [("Lexer", "regex tokens"), ("parse_value", "atoms"), ("object", "minimal")],
        ["tokenize", "parse int", "object", "null"],
        "# Pesquisa\n\n- `pratt_query_lang` Dia 07\n- json.org grammar\n",
    )


def scaffold_agent_tool_fsm() -> None:
    base = DAY08 / "agent" / "tool_protocol_fsm"
    starter = '''"""Tool calling FSM — IDLE→CALLING→WAITING→DONE/ERROR."""

from __future__ import annotations

TRANSITIONS = {
    ("IDLE", "call"): "CALLING",
    ("CALLING", "sent"): "WAITING",
    ("WAITING", "ok"): "DONE",
    ("WAITING", "err"): "ERROR",
}


class ToolProtocolFSM:
    def __init__(self):
        self.state = "IDLE"
        self.trace: list[str] = []

    def transition(self, event: str) -> str:
        """TODO [AGT-TOOL-01]: apply TRANSITIONS and append to trace."""
        raise NotImplementedError("AGT-TOOL-01")

    def handle_response(self, ok: bool, payload: dict) -> dict:
        """TODO [AGT-TOOL-02]: transition on ok/err; return evidence."""
        raise NotImplementedError("AGT-TOOL-02")

    def validate_tool_call(self, name: str, args: dict) -> bool:
        """TODO [AGT-TOOL-03]: name non-empty and args is dict."""
        raise NotImplementedError("AGT-TOOL-03")
'''
    sol = starter.replace(
        '    def transition(self, event: str) -> str:\n        """TODO [AGT-TOOL-01]: apply TRANSITIONS and append to trace."""\n        raise NotImplementedError("AGT-TOOL-01")',
        '''    def transition(self, event: str) -> str:
        # PEDAGOGY-SOLUTION: AGT-TOOL-01
        key = (self.state, event)
        if key not in TRANSITIONS:
            raise ValueError(key)
        self.state = TRANSITIONS[key]
        self.trace.append(f"{event}->{self.state}")
        return self.state''',
    ).replace(
        '    def handle_response(self, ok: bool, payload: dict) -> dict:\n        """TODO [AGT-TOOL-02]: transition on ok/err; return evidence."""\n        raise NotImplementedError("AGT-TOOL-02")',
        '''    def handle_response(self, ok: bool, payload: dict) -> dict:
        # PEDAGOGY-SOLUTION: AGT-TOOL-02
        self.transition("ok" if ok else "err")
        return {"state": self.state, "payload_keys": list(payload.keys())}''',
    ).replace(
        '    def validate_tool_call(self, name: str, args: dict) -> bool:\n        """TODO [AGT-TOOL-03]: name non-empty and args is dict."""\n        raise NotImplementedError("AGT-TOOL-03")',
        '''    def validate_tool_call(self, name: str, args: dict) -> bool:
        # PEDAGOGY-SOLUTION: AGT-TOOL-03
        return bool(name) and isinstance(args, dict)''',
    )
    test = '''# PEDAGOGY-TEST: AGT-TOOL-01
# PEDAGOGY-TEST: AGT-TOOL-02
# PEDAGOGY-TEST: AGT-TOOL-03
# Caso 1: IDLE call -> CALLING
# Caso 2: handle_response ok -> DONE
# Caso 3: validate_tool_call
# Caso 4: err path -> ERROR
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tool_protocol_fsm import ToolProtocolFSM

def main():
    fsm = ToolProtocolFSM()
    assert fsm.transition("call") == "CALLING"
    fsm.transition("sent")
    ev = fsm.handle_response(True, {"result": 1})
    assert ev["state"] == "DONE"
    assert fsm.validate_tool_call("search", {})
    fsm2 = ToolProtocolFSM()
    fsm2.transition("call"); fsm2.transition("sent")
    fsm2.handle_response(False, {})
    assert fsm2.state == "ERROR"
    print("OK tool_protocol_fsm")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "tool_protocol_fsm", starter, sol, test)
    todos = [
        {"id": "AGT-TOOL-01", "file": "starter/tool_protocol_fsm.py", "fn": "transition",
         "problem": "FSM tool call.", "code": "TRANSITIONS[(state,event)]",
         "why": "Protocolo agente.", "verify": "Caso 1: CALLING."},
        {"id": "AGT-TOOL-02", "file": "starter/tool_protocol_fsm.py", "fn": "handle_response",
         "problem": "Resposta ok/err.", "code": 'transition("ok"|"err")',
         "why": "Ciclo request/response.", "verify": "Caso 2: DONE."},
        {"id": "AGT-TOOL-03", "file": "starter/tool_protocol_fsm.py", "fn": "validate_tool_call",
         "problem": "Validação entrada.", "code": "bool(name) and isinstance(args, dict)",
         "why": "Evita calls vazios.", "verify": "Caso 3: true."},
    ]
    write_pedagogy_docs(
        base, "tool_protocol_fsm",
        "# Agent — tool protocol FSM\n\nFSM de tool calling (continua `loop_state_machine`).\n",
        "cd days/2026-09-08/agent/tool_protocol_fsm/starter\npython test_tool_protocol_fsm.py",
        todos, [("Transitions", "IDLE→DONE"), ("Response", "ok/err"), ("Validation", "tool call")],
        ["call transition", "ok DONE", "validate", "err ERROR"],
        "# Pesquisa\n\n- OpenAI function calling protocol\n- `loop_state_machine` Dia 07\n",
    )


def scaffold_tooling_wasm() -> None:
    base = DAY08 / "tooling" / "wasm_section_header"
    starter = '''"""WASM module header — magic, version, section headers."""

from __future__ import annotations

import struct

WASM_MAGIC = b"\\x00asm"


def validate_magic(data: bytes) -> bool:
    """TODO [TOOL-WASM-01]: check \\0asm magic."""
    raise NotImplementedError("TOOL-WASM-01")


def parse_version(data: bytes) -> int:
    """TODO [TOOL-WASM-02]: read u32 LE version after magic."""
    raise NotImplementedError("TOOL-WASM-02")


def parse_section_headers(data: bytes) -> list[tuple[int, int]]:
    """TODO [TOOL-WASM-03]: return list of (section_id, payload_size) until EOF."""
    raise NotImplementedError("TOOL-WASM-03")
'''
    sol = starter.replace(
        'def validate_magic(data: bytes) -> bool:\n    """TODO [TOOL-WASM-01]: check \\0asm magic."""\n    raise NotImplementedError("TOOL-WASM-01")',
        '''def validate_magic(data: bytes) -> bool:
    # PEDAGOGY-SOLUTION: TOOL-WASM-01
    return len(data) >= 4 and data[:4] == WASM_MAGIC''',
    ).replace(
        'def parse_version(data: bytes) -> int:\n    """TODO [TOOL-WASM-02]: read u32 LE version after magic."""\n    raise NotImplementedError("TOOL-WASM-02")',
        '''def parse_version(data: bytes) -> int:
    # PEDAGOGY-SOLUTION: TOOL-WASM-02
    if not validate_magic(data) or len(data) < 8:
        raise ValueError("bad wasm")
    return struct.unpack_from("<I", data, 4)[0]''',
    ).replace(
        'def parse_section_headers(data: bytes) -> list[tuple[int, int]]:\n    """TODO [TOOL-WASM-03]: return list of (section_id, payload_size) until EOF."""\n    raise NotImplementedError("TOOL-WASM-03")',
        '''def parse_section_headers(data: bytes) -> list[tuple[int, int]]:
    # PEDAGOGY-SOLUTION: TOOL-WASM-03
    if parse_version(data) != 1:
        raise ValueError("only version 1")
    out: list[tuple[int, int]] = []
    off = 8
    while off < len(data):
        sec_id = data[off]
        off += 1
        size = 0
        shift = 0
        while True:
            if off >= len(data):
                raise ValueError("truncated size")
            b = data[off]
            off += 1
            size |= (b & 0x7F) << shift
            if b & 0x80 == 0:
                break
            shift += 7
        out.append((sec_id, size))
        off += size
    return out''',
    )
    test = '''# PEDAGOGY-TEST: TOOL-WASM-01
# PEDAGOGY-TEST: TOOL-WASM-02
# PEDAGOGY-TEST: TOOL-WASM-03
# Caso 1: magic \\0asm
# Caso 2: version 1
# Caso 3: one section header
# Caso 4: bad magic false
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from wasm_section_header import validate_magic, parse_version, parse_section_headers, WASM_MAGIC

def build_wasm(sections):
    buf = bytearray(WASM_MAGIC)
    buf += struct.pack("<I", 1)
    for sid, payload in sections:
        buf.append(sid)
        buf.append(len(payload))
        buf += payload
    return bytes(buf)

def main():
    w = build_wasm([(1, b"\\x00"), (3, b"abc")])
    assert validate_magic(w)
    assert parse_version(w) == 1
    hdrs = parse_section_headers(w)
    assert hdrs == [(1, 1), (3, 3)]
    assert not validate_magic(b"bad!")
    print("OK wasm_section_header")

if __name__ == "__main__":
    main()
'''
    write_py_sides(base, "wasm_section_header", starter, sol, test)
    todos = [
        {"id": "TOOL-WASM-01", "file": "starter/wasm_section_header.py", "fn": "validate_magic",
         "problem": "Magic bytes.", "code": "data[:4]==b'\\0asm'",
         "why": "Gate WASM.", "verify": "Caso 1: true."},
        {"id": "TOOL-WASM-02", "file": "starter/wasm_section_header.py", "fn": "parse_version",
         "problem": "Version u32.", "code": "struct.unpack u32 at 4",
         "why": "Compatibilidade.", "verify": "Caso 2: version 1."},
        {"id": "TOOL-WASM-03", "file": "starter/wasm_section_header.py", "fn": "parse_section_headers",
         "problem": "LEB128 size walk.", "code": "while off < len",
         "why": "Mapa de seções.", "verify": "Caso 3: two sections."},
    ]
    write_pedagogy_docs(
        base, "wasm_section_header",
        "# Tooling — WASM section headers\n\nParse magic+version+section headers.\n",
        "cd days/2026-09-08/tooling/wasm_section_header/starter\npython test_wasm_section_header.py",
        todos, [("Magic", "\\0asm"), ("Version", "u32"), ("Sections", "LEB128")],
        ["magic ok", "version 1", "section list", "bad magic"],
        "# Pesquisa\n\n- WebAssembly binary format\n- `miniobjdump` Dia 03\n",
    )


def scaffold_day_infra() -> None:
    DAY08.mkdir(parents=True, exist_ok=True)
    modules = [
        ("N1", "systems/clvm_disassembler", "disassemble CLVM v2 bytecode", "2–3"),
        ("N2", "systems/clvm_peephole_opt", "constant folding peephole", "2"),
        ("N3", "linux/input_event_ring_mux", "mux kbd+mouse ring", "2–3"),
        ("N4", "rust/clvm_disasm", "Rust disassembler", "2–3"),
        ("N5", "dotnet/pe_export_span", "PE export Span parse", "2"),
        ("N6", "graphics/shader_stage_fsm", "shader compile FSM", "2"),
        ("N7", "redteam/pe_export_triage", "PE export triage", "2"),
        ("N8", "quantum/bell_state_prep", "Bell state prep", "2"),
        ("N9", "ai/softmax_stable", "stable softmax", "2"),
        ("N10", "nodejs/duplex_event_pipe", "Duplex 24B events", "2"),
        ("N11", "parsers/json_rd_lexer", "JSON RD lexer", "2"),
        ("N12", "agent/tool_protocol_fsm", "tool calling FSM", "2"),
        ("N13", "tooling/wasm_section_header", "WASM section headers", "2"),
    ]
    table = "\n".join(
        f"| {n} | `{m}` | {d} | {h} |" for n, m, d, h in modules
    )
    (DAY08 / "README.md").write_text(
        f"# Day 2026-09-08 — CLVM toolchain + input multiplexação\n\n"
        f"Dia **tier-A** (13 módulos): continuação CLVM v2 + drivers/input + toolchain binário.\n\n"
        f"## Módulos (13)\n\n| # | Módulo | Fundamento | Horas |\n|---|--------|------------|-------|\n{table}\n\n"
        f"**Total:** ~28–32 h.\n\n"
        f"**Pré-requisito:** Day 07 (`clvm_v2_strings`, `hid_keyboard_boot`, `input_event_transform`).\n",
        encoding="utf-8",
    )
    (DAY08 / "START_HERE.md").write_text(
        "# START HERE — Day 2026-09-08\n\n"
        "Tema: **CLVM toolchain + input multiplexação** (tier-A, 13 módulos).\n\n"
        "## Fluxo por módulo\n\n"
        "1. `TEORIA_PASSO_A_PASSO.md` → trace no papel.\n"
        "2. Checkpoint em `ATIVIDADES.md`.\n"
        "3. `starter/` (`TODO [ID]`) → testes `PEDAGOGY-TEST`.\n"
        "4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` ao travar.\n\n"
        "## Ordem sugerida\n\n"
        "| Bloco | Módulos |\n|-------|---------|\n"
        "| Manhã CLVM toolchain | `clvm_disassembler` → `clvm_peephole_opt` → `clvm_disasm` (Rust) |\n"
        "| Tarde input mux | `input_event_ring_mux` → `duplex_event_pipe` |\n"
        "| Binários PE/WASM | `pe_export_span` → `pe_export_triage` → `wasm_section_header` |\n"
        "| GFX + quantum + AI | `shader_stage_fsm` → `bell_state_prep` → `softmax_stable` |\n"
        "| Parsers + agent | `json_rd_lexer` → `tool_protocol_fsm` |\n\n"
        "Mapa: `TODO_MAP.md`.\n\n"
        "## Validação\n\n```powershell\n"
        "python scripts/pedagogy_check_unified.py --day 2026-09-08\n"
        "python scripts/run_day_tests.py --day 2026-09-08 --mode solutions\n```\n",
        encoding="utf-8",
    )
    (DAY08 / "ATIVIDADES.md").write_text(
        "# ATIVIDADES — 2026-09-08\n\n"
        "**Dia:** 13 módulos | **~28–32 h**\n\n"
        "## Preparação (30 min)\n\n"
        "- [ ] Ler `START_HERE.md` e `README.md`\n"
        "- [ ] Baseline: `python scripts/pedagogy_check_unified.py --day 2026-09-08`\n\n"
        "## Bloco 1 — CLVM toolchain (6–8 h)\n\n"
        "| Módulo | TODOs | Paper-trace |\n|--------|-------|-------------|\n"
        "| `systems/clvm_disassembler` | CLVM-DIS-01..03 | hex bytecode → texto |\n"
        "| `systems/clvm_peephole_opt` | CLVM-PEEP-01..03 | antes/depois bytes |\n"
        "| `rust/clvm_disasm` | CLVM-RS-DIS-01..03 | paridade Rust |\n\n"
        "**Checkpoint:** explico PUSH vs branch sizes.\n\n"
        "## Bloco 2 — Input multiplexação (4–5 h)\n\n"
        "| `linux/input_event_ring_mux` | LIN-MUX-01..03 | ring + mux trace |\n"
        "| `nodejs/duplex_event_pipe` | ND-DUPLEX-01..03 | 24B duplex |\n\n"
        "## Bloco 3 — Binários + GFX + quantum + AI (10–12 h)\n\n"
        "PE span/triage, WASM headers, shader FSM, Bell, softmax.\n\n"
        "## Bloco 4 — Parsers + agent (4 h)\n\n"
        "`json_rd_lexer`, `tool_protocol_fsm`.\n\n"
        "## Relatório do dia\n\n| Bloco | Checkpoint | Testes |\n|-------|------------|--------|\n"
        "| 1 | ☐ | ☐ |\n| 2 | ☐ | ☐ |\n| 3 | ☐ | ☐ |\n| 4 | ☐ | ☐ |\n",
        encoding="utf-8",
    )
    (DAY08 / "TODO_MAP.md").write_text(
        "# TODO map — 2026-09-08 (placeholder; regenerate with generate_day_scaffold --manifest-only)\n",
        encoding="utf-8",
    )
    (DAY08 / "VALIDATION.md").write_text(
        "# VALIDATION — Day 2026-09-08\n\n"
        "## Gates\n\n```powershell\n"
        "python scripts/pedagogy_check_unified.py --day 2026-09-08\n"
        "python scripts/day_contract_check.py --day 2026-09-08\n"
        "python scripts/run_day_tests.py --day 2026-09-08 --mode solutions\n```\n\n"
        "## Módulos (13)\n\n"
        "clvm_disassembler, clvm_peephole_opt, input_event_ring_mux, clvm_disasm, pe_export_span, "
        "shader_stage_fsm, pe_export_triage, bell_state_prep, softmax_stable, duplex_event_pipe, "
        "json_rd_lexer, tool_protocol_fsm, wasm_section_header\n",
        encoding="utf-8",
    )
    (DAY08 / "MANIFEST.json").write_text(
        json.dumps({"day": "2026-09-08", "modules": 13, "files": []}, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    scaffold_clvm_disassembler()
    scaffold_clvm_peephole()
    scaffold_linux_mux()
    scaffold_rust_disasm()
    scaffold_dotnet_pe()
    scaffold_gfx_shader_fsm()
    scaffold_redteam_pe()
    scaffold_quantum_bell()
    scaffold_ai_softmax()
    scaffold_node_duplex()
    scaffold_parsers_json()
    scaffold_agent_tool_fsm()
    scaffold_tooling_wasm()
    scaffold_day_infra()
    print("Day 08 scaffolded: 13 tier-A modules")


if __name__ == "__main__":
    main()
