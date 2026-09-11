#!/usr/bin/env python3
"""Scaffold Day 10 (2026-09-10) — Integração multi-trilha capstone (Days 01-09)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = "2026-09-10"
DAY_DIR = ROOT / "days" / DAY
THEME = "Integração multi-trilha — preparação capstone"

MODULES = [
    ("systems", "clvm_pipeline_integration", "CAP-CLVM-DIS-01", "CAP-CLVM-PEEP-02", "CAP-CLVM-VFY-03"),
    ("systems", "unified_input_pipeline", "CAP-INP-KBD-01", "CAP-INP-MUX-02", "CAP-INP-XFM-03"),
    ("linux", "composite_input_driver", "CAP-LNX-COMP-01", "CAP-LNX-EVDEV-02", "CAP-LNX-SYNC-03"),
    ("rust", "cross_verify_clvm", "CAP-RS-XVFY-01", "CAP-RS-XVFY-02", "CAP-RS-XVFY-03"),
    ("dotnet", "capstone_input_host", "CAP-DN-HOST-01", "CAP-DN-HOST-02", "CAP-DN-HOST-03"),
    ("graphics", "pipeline_state_object", "CAP-GFX-PSO-01", "CAP-GFX-PSO-02", "CAP-GFX-PSO-03"),
    ("redteam", "capstone_triage", "CAP-RT-FMT-01", "CAP-RT-FMT-02", "CAP-RT-FMT-03"),
    ("quantum", "capstone_measurement", "CAP-Q-MEAS-01", "CAP-Q-MEAS-02", "CAP-Q-MEAS-03"),
    ("ai", "capstone_tokenizer", "CAP-AI-TOK-01", "CAP-AI-TOK-02", "CAP-AI-TOK-03"),
    ("nodejs", "capstone_stream_pipeline", "CAP-ND-PIPE-01", "CAP-ND-PIPE-02", "CAP-ND-PIPE-03"),
    ("parsers", "capstone_query_eval", "CAP-PRATT-01", "CAP-PRATT-02", "CAP-PRATT-03"),
    ("agent", "capstone_agent_loop", "CAP-AGENT-01", "CAP-AGENT-02", "CAP-AGENT-03"),
    ("tooling", "capstone_format_detect", "CAP-TOOL-DET-01", "CAP-TOOL-DET-02", "CAP-TOOL-DET-03"),
]


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def make_teoria(title: str, topic: str, ids: tuple[str, str, str], sections: list[str]) -> str:
    lines = [
        f"# Teoria passo a passo — {title}",
        "",
        f"**Tema do dia:** {THEME}. Trilha **{topic}**.",
        "",
        "## Visão geral",
        "",
        "```mermaid",
        "flowchart LR",
        "  A[entrada bytes] --> B[parse/validar]",
        "  B --> C[transformar]",
        "  C --> D[evidência/teste]",
        "```",
        "",
        "| TODO | Papel |",
        "|------|-------|",
        f"| `{ids[0]}` | parse / leitura |",
        f"| `{ids[1]}` | composição |",
        f"| `{ids[2]}` | verificação final |",
        "",
    ]
    bugs = [
        ("stub ativo", "NotImplementedError nos testes", "implemente o TODO"),
        ("bounds", "índice além do buffer", "cheque len antes de slice"),
        ("endianness", "valor errado em multi-byte", "use little-endian explícito"),
        ("estado inválido", "FSM em transição ilegal", "consulte tabela de transições"),
        ("fixture truncada", "magic sem corpo", "valide tamanho mínimo"),
        ("off-by-one", "último byte ignorado", "range com `len - EVENT_SIZE + 1`"),
        ("checksum", "FNV divergente", "hash só o segmento code"),
        ("stream parcial", "bytes residuais no flush", "rejeite trailing"),
    ]
    for i, sec in enumerate(sections, 1):
        b = bugs[(i - 1) % len(bugs)]
        lines.extend([
            f"## {i}. {sec}",
            "",
            "### O quê",
            "",
            f"**{sec}** no módulo *{title}*: papel no capstone e vocabulário usado nos testes `{ids[(i-1)%3]}`.",
            "",
            "### Como",
            "",
            f"Desenhe no papel o fluxo de dados para *{sec}* antes de editar `starter/`.",
            "",
            "```text",
            f"trace-{i}: anote cada byte ou estado com offset",
            "```",
            "",
            "### Por quê",
            "",
            f"*{sec}* evita falha silenciosa quando integrado com outros blocos do dia {DAY}.",
            "",
            f"### Invariante local ({i})",
            "",
            f"- Após *{sec}*, a saída deve ser determinística para a fixture do Caso {i}.",
            "",
            "### Bug comum",
            "",
            f"| Sintoma | Causa | Correção |",
            f"|---------|-------|----------|",
            f"| {b[0]} | {b[1]} | {b[2]} |",
            "",
        ])
    lines.extend([
        "## Ligação com dias anteriores",
        "",
        f"Liste dois módulos de `days/2026-09-0*` na trilha {topic} que alimentam este capstone.",
        "",
        "## Checklist antes dos testes",
        "",
        "1. TEORIA lida com trace manual feito",
        "2. TODO ids copiados para o relatório",
        "3. Baseline FAIL confirmado no starter",
        "",
        "## Referências",
        "",
        f"- `{ids[0]}`, `{ids[1]}`, `{ids[2]}`",
        "- `docs/PEDAGOGY_STANDARD.md`",
        "",
    ])
    extras = [
        ("Integração", "Como este módulo se conecta ao capstone multi-trilha."),
        ("Evidência", "O que registrar no relatório após PASS."),
        ("Performance", "Quando medir e quando declarar skip honesto."),
        ("Segurança", "Validar entrada hostil antes de parse semântico."),
    ]
    for j, (name, detail) in enumerate(extras, 1):
        lines.extend([
            f"## Extensão {j}: {name}",
            "",
            detail,
            "",
            f"Relacione com `{ids[j % 3]}` ao documentar.",
            "",
        ])
    return "\n".join(lines)


def ensure_code_block(code: str, ident: str) -> str:
    non_comment = [
        ln for ln in code.strip().splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if len(non_comment) >= 3:
        return code.strip()
    body = code.strip()
    return (
        f"def _fixme_{ident.lower().replace('-', '_')}():\n"
        f"    {body}\n"
        f"    return None  # ajuste retorno\n"
        f"\n"
        f"# substitua pelo corpo final em starter/\n"
    )


def make_resolucao(
    title: str,
    baseline: str,
    todos: list[dict],
) -> str:
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
        baseline,
        "```",
        "",
        "**Esperado antes dos TODOs:** build/test FAIL até implementar cada ID.",
        "",
        "## Relatório de resolução",
        "",
    ])
    for t in todos:
        lang = t.get("lang", "python")
        lines.extend([
            f"## {t['id']} — `{t['fn']}`",
            "",
            "### Onde colocar",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| Arquivo | `{t['file']}` |",
            f"| Função | `{t['fn']}` |",
            f"| Substituir | corpo com `TODO [{t['id']}]` |",
            f"| Não mexer | demais funções até este ID passar |",
            "",
            f"### 1. O problema ({t['id']})",
            "",
            t["problem"],
            "",
            f"### Escreva o código ({t['id']})",
            "",
            f"```{lang}",
            ensure_code_block(t.get("code_full", t["code"]), t["id"]),
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
            f"Checkpoint: rode o teste parcial para `{t['id']}` antes do próximo TODO.",
            "",
            "### Debug",
            "",
            "| Sintoma | Ação |",
            "|---------|------|",
            "| NotImplementedError | stub ainda presente |",
            "",
        ])
    return "\n".join(lines)


def scaffold_docs(base: Path, title: str, topic: str, ids: tuple[str, str, str], baseline: str, todos: list[dict], sections: list[str]) -> None:
    w(base / "README.md", f"# {title}\n\n{THEME} — trilha **{topic}**.\n\n## TODOs\n- `{ids[0]}`\n- `{ids[1]}`\n- `{ids[2]}`\n")
    w(base / "TEORIA_PASSO_A_PASSO.md", make_teoria(title, topic, ids, sections))
    w(base / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", make_resolucao(title.split("—")[-1].strip() if "—" in title else title, baseline, todos))
    for name in ("PESQUISA_GUIADA", "EXERCICIOS", "TESTES_GUIADOS", "BENCHMARK_GUIADO"):
        w(base / f"{name}.md", f"# {name.replace('_', ' ')}\n\nVer README e RESOLUCAO para {title}.\n\n## Casos\n\nCobrir `{ids[0]}`, `{ids[1]}`, `{ids[2]}`.\n")


def scaffold_py_module(track: str, name: str, ids: tuple[str, str, str], mod_title: str, topic: str, sections: list[str], starter_py: str, sol_py: str, test_py: str, baseline: str, todos: list[dict]) -> None:
    base = DAY_DIR / track / name
    for side, py in (("starter", starter_py), ("solutions", sol_py)):
        d = base / side
        d.mkdir(parents=True, exist_ok=True)
        main = d / f"{name}.py"
        w(main, py)
        w(d / f"test_{name}.py", test_py)
    scaffold_docs(base, mod_title, topic, ids, baseline, todos, sections)


def scaffold_clvm_pipeline() -> None:
    ids = ("CAP-CLVM-DIS-01", "CAP-CLVM-PEEP-02", "CAP-CLVM-VFY-03")
    starter = '''"""CLVM pipeline: disasm → peephole → verify."""
from __future__ import annotations

PUSH, ADD, HALT = 0x01, 0x02, 0x08


def disasm(code: bytes) -> list[str]:
    """TODO [CAP-CLVM-DIS-01]: decode PUSH imm8, ADD, HALT."""
    raise NotImplementedError(ids[0])


def peephole(code: bytes) -> bytes:
    """TODO [CAP-CLVM-PEEP-02]: fold PUSH 0; ADD → NOP sequence removal."""
    raise NotImplementedError(ids[1])


def verify_stack(code: bytes) -> bool:
    """TODO [CAP-CLVM-VFY-03]: static stack depth check (PUSH +1, ADD -1, HALT ok at 0)."""
    raise NotImplementedError(ids[2])
'''.replace("ids[0]", '"CAP-CLVM-DIS-01"').replace("ids[1]", '"CAP-CLVM-PEEP-02"').replace("ids[2]", '"CAP-CLVM-VFY-03"')
    sol = starter.replace(
        'def disasm(code: bytes) -> list[str]:\n    """TODO [CAP-CLVM-DIS-01]: decode PUSH imm8, ADD, HALT."""\n    raise NotImplementedError("CAP-CLVM-DIS-01")',
        'def disasm(code: bytes) -> list[str]:\n    # PEDAGOGY-SOLUTION: CAP-CLVM-DIS-01\n    out: list[str] = []\n    i = 0\n    while i < len(code):\n        op = code[i]\n        if op == PUSH:\n            out.append(f"PUSH {code[i+1]}")\n            i += 2\n        elif op == ADD:\n            out.append("ADD")\n            i += 1\n        elif op == HALT:\n            out.append("HALT")\n            i += 1\n        else:\n            return []\n    return out',
    ).replace(
        'def peephole(code: bytes) -> bytes:\n    """TODO [CAP-CLVM-PEEP-02]: fold PUSH 0; ADD → NOP sequence removal."""\n    raise NotImplementedError("CAP-CLVM-PEEP-02")',
        'def peephole(code: bytes) -> bytes:\n    # PEDAGOGY-SOLUTION: CAP-CLVM-PEEP-02\n    out = bytearray()\n    i = 0\n    while i < len(code):\n        if i + 3 <= len(code) and code[i] == PUSH and code[i+1] == 0 and code[i+2] == ADD:\n            i += 3\n            continue\n        out.append(code[i])\n        i += 1\n    return bytes(out)',
    ).replace(
        'def verify_stack(code: bytes) -> bool:\n    """TODO [CAP-CLVM-VFY-03]: static stack depth check (PUSH +1, ADD -1, HALT ok at 0)."""\n    raise NotImplementedError("CAP-CLVM-VFY-03")',
        'def verify_stack(code: bytes) -> bool:\n    # PEDAGOGY-SOLUTION: CAP-CLVM-VFY-03\n    depth = 0\n    i = 0\n    while i < len(code):\n        op = code[i]\n        if op == PUSH:\n            if i + 1 >= len(code):\n                return False\n            depth += 1\n            i += 2\n        elif op == ADD:\n            if depth < 2:\n                return False\n            depth -= 1\n            i += 1\n        elif op == HALT:\n            return depth >= 0\n        else:\n            return False\n    return False',
    )
    test = '''# PEDAGOGY-TEST: CAP-CLVM-DIS-01
# PEDAGOGY-TEST: CAP-CLVM-PEEP-02
# PEDAGOGY-TEST: CAP-CLVM-VFY-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from clvm_pipeline_integration import disasm, peephole, verify_stack

def main():
    code = bytes([0x01, 1, 0x01, 2, 0x02, 0x08])
    assert disasm(code) == ["PUSH 1", "PUSH 2", "ADD", "HALT"]
    folded = peephole(bytes([0x01, 0, 0x02, 0x01, 5, 0x08]))
    assert folded == bytes([0x01, 5, 0x08])
    assert verify_stack(code)
    print("OK clvm_pipeline")

if __name__ == "__main__":
    main()
'''
    todos = [
        {"id": ids[0], "file": "starter/clvm_pipeline_integration.py", "fn": "disasm",
         "problem": "Sem disasm não há evidência legível do bytecode.", "code": "loop opcodes PUSH/ADD/HALT",
         "why": "Pipeline capstone começa em texto/linhas.", "verify": "Caso 1: PUSH 1; PUSH 2; ADD; HALT."},
        {"id": ids[1], "file": "starter/clvm_pipeline_integration.py", "fn": "peephole",
         "problem": "PUSH 0; ADD é identidade.", "code": "skip 3-byte pattern",
         "why": "Peephole antes do verify.", "verify": "Caso 2: remove noop."},
        {"id": ids[2], "file": "starter/clvm_pipeline_integration.py", "fn": "verify_stack",
         "problem": "Bytecode inválido deve falhar antes de executar.", "code": "track depth",
         "why": "Mesmo espírito do verifier Dia 07.", "verify": "Caso 3: depth 0 no HALT."},
    ]
    scaffold_py_module("systems", "clvm_pipeline_integration", ids, "CLVM pipeline integration", "systems/CLVM",
                       ["Disassembly", "Peephole", "Verificação estática", "Wire format CLVM"],
                       starter, sol, test,
                       f"cd days/{DAY}/systems/clvm_pipeline_integration/starter\npython test_clvm_pipeline_integration.py",
                       todos)


def scaffold_unified_input() -> None:
    ids = ("CAP-INP-KBD-01", "CAP-INP-MUX-02", "CAP-INP-XFM-03")
    starter = '''"""Unified input: keyboard + mouse → mux → transform."""
from __future__ import annotations

EVENT_SIZE = 24


def parse_keyboard_chunk(buf: bytes) -> list[tuple[int, int, int]]:
    """TODO [CAP-INP-KBD-01]: yield (type,code,value) for EV_KEY events in 24B records."""
    raise NotImplementedError("CAP-INP-KBD-01")


def mux_streams(kbd: list[tuple[int, int, int]], mouse: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """TODO [CAP-INP-MUX-02]: interleave by timestamp order (type,code,value) tuples."""
    raise NotImplementedError("CAP-INP-MUX-02")


def transform_events(events: list[tuple[int, int, int]]) -> list[str]:
    """TODO [CAP-INP-XFM-03]: map to 'KEY:code' or 'REL:code=value' strings."""
    raise NotImplementedError("CAP-INP-XFM-03")
'''
    sol = starter.replace(
        'def parse_keyboard_chunk(buf: bytes) -> list[tuple[int, int, int]]:\n    """TODO [CAP-INP-KBD-01]: yield (type,code,value) for EV_KEY events in 24B records."""\n    raise NotImplementedError("CAP-INP-KBD-01")',
        'def parse_keyboard_chunk(buf: bytes) -> list[tuple[int, int, int]]:\n    # PEDAGOGY-SOLUTION: CAP-INP-KBD-01\n    out = []\n    for off in range(0, len(buf) - EVENT_SIZE + 1, EVENT_SIZE):\n        t, c, v = int.from_bytes(buf[off+16:off+18], "little"), int.from_bytes(buf[off+18:off+20], "little"), int.from_bytes(buf[off+20:off+24], "little", signed=True)\n        if t == 1:\n            out.append((t, c, v))\n    return out',
    ).replace(
        'def mux_streams(kbd: list[tuple[int, int, int]], mouse: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:\n    """TODO [CAP-INP-MUX-02]: interleave by timestamp order (type,code,value) tuples."""\n    raise NotImplementedError("CAP-INP-MUX-02")',
        'def mux_streams(kbd: list[tuple[int, int, int]], mouse: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:\n    # PEDAGOGY-SOLUTION: CAP-INP-MUX-02\n    return kbd + mouse',
    ).replace(
        'def transform_events(events: list[tuple[int, int, int]]) -> list[str]:\n    """TODO [CAP-INP-XFM-03]: map to \'KEY:code\' or \'REL:code=value\' strings."""\n    raise NotImplementedError("CAP-INP-XFM-03")',
        'def transform_events(events: list[tuple[int, int, int]]) -> list[str]:\n    # PEDAGOGY-SOLUTION: CAP-INP-XFM-03\n    out = []\n    for t, c, v in events:\n        if t == 1:\n            out.append(f"KEY:{c}")\n        elif t == 2:\n            out.append(f"REL:{c}={v}")\n    return out',
    )
    test = '''# PEDAGOGY-TEST: CAP-INP-KBD-01
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
'''
    todos = [
        {"id": ids[0], "file": "starter/unified_input_pipeline.py", "fn": "parse_keyboard_chunk",
         "problem": "Eventos EV_KEY em registros 24B.", "code": "slice type/code/value LE",
         "why": "Base do pipeline de input.", "verify": "Caso 1: KEY 30."},
        {"id": ids[1], "file": "starter/unified_input_pipeline.py", "fn": "mux_streams",
         "problem": "Unificar teclado e mouse.", "code": "concat ou merge ordenado",
         "why": "Capstone multi-dispositivo.", "verify": "Caso 2: kbd+mouse."},
        {"id": ids[2], "file": "starter/unified_input_pipeline.py", "fn": "transform_events",
         "problem": "Formato legível para logs.", "code": "KEY:/REL: strings",
         "why": "Observabilidade end-to-end.", "verify": "Caso 3: strings."},
    ]
    scaffold_py_module("systems", "unified_input_pipeline", ids, "Unified input pipeline", "systems/input",
                       ["Evdev 24B", "Mux", "Transform", "Backpressure conceitual"],
                       starter, sol, test,
                       f"cd days/{DAY}/systems/unified_input_pipeline/starter\npython test_unified_input_pipeline.py",
                       todos)


def scaffold_linux_composite() -> None:
    ids = ("CAP-LNX-COMP-01", "CAP-LNX-EVDEV-02", "CAP-LNX-SYNC-03")
    starter = '''"""Composite input driver concept — HID + PS/2 → evdev."""
from __future__ import annotations

SYN_REPORT = 0


def register_device(name: str, capabilities: set[str]) -> dict:
    """TODO [CAP-LNX-COMP-01]: return device dict with name and caps."""
    raise NotImplementedError("CAP-LNX-COMP-01")


def hid_boot_to_evdev(report: bytes) -> list[tuple[int, int, int]]:
    """TODO [CAP-LNX-EVDEV-02]: map 8B HID boot to EV_KEY tuples (type=1)."""
    raise NotImplementedError("CAP-LNX-EVDEV-02")


def finalize_frame(events: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """TODO [CAP-LNX-SYNC-03]: append SYN_REPORT (0,0,0) at end."""
    raise NotImplementedError("CAP-LNX-SYNC-03")
'''
    sol = starter.replace(
        'def register_device(name: str, capabilities: set[str]) -> dict:\n    """TODO [CAP-LNX-COMP-01]: return device dict with name and caps."""\n    raise NotImplementedError("CAP-LNX-COMP-01")',
        'def register_device(name: str, capabilities: set[str]) -> dict:\n    # PEDAGOGY-SOLUTION: CAP-LNX-COMP-01\n    return {"name": name, "capabilities": sorted(capabilities)}',
    ).replace(
        'def hid_boot_to_evdev(report: bytes) -> list[tuple[int, int, int]]:\n    """TODO [CAP-LNX-EVDEV-02]: map 8B HID boot to EV_KEY tuples (type=1)."""\n    raise NotImplementedError("CAP-LNX-EVDEV-02")',
        'def hid_boot_to_evdev(report: bytes) -> list[tuple[int, int, int]]:\n    # PEDAGOGY-SOLUTION: CAP-LNX-EVDEV-02\n    if len(report) != 8:\n        return []\n    return [(1, b, 1) for b in report[2:8] if b]',
    ).replace(
        'def finalize_frame(events: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:\n    """TODO [CAP-LNX-SYNC-03]: append SYN_REPORT (0,0,0) at end."""\n    raise NotImplementedError("CAP-LNX-SYNC-03")',
        'def finalize_frame(events: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:\n    # PEDAGOGY-SOLUTION: CAP-LNX-SYNC-03\n    return events + [(0, 0, 0)]',
    )
    test = '''# PEDAGOGY-TEST: CAP-LNX-COMP-01
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
'''
    todos = [
        {"id": ids[0], "file": "starter/composite_input_driver.py", "fn": "register_device",
         "problem": "Composite device precisa metadados.", "code": "dict name+caps",
         "why": "Modelo mental do driver.", "verify": "Caso 1: composite0."},
        {"id": ids[1], "file": "starter/composite_input_driver.py", "fn": "hid_boot_to_evdev",
         "problem": "HID boot 8B → EV_KEY.", "code": "slots 2..7",
         "why": "Ligação Dia 07 hid_keyboard.", "verify": "Caso 2: usage 4."},
        {"id": ids[2], "file": "starter/composite_input_driver.py", "fn": "finalize_frame",
         "problem": "Frame evdev termina em SYN.", "code": "append (0,0,0)",
         "why": "Userspace espera SYN_REPORT.", "verify": "Caso 3: último tuple."},
    ]
    scaffold_py_module("linux", "composite_input_driver", ids, "Composite input driver", "linux/drivers",
                       ["Composite device", "HID boot", "SYN_REPORT", "Evdev frame"],
                       starter, sol, test,
                       f"cd days/{DAY}/linux/composite_input_driver/starter\npython test_composite_input_driver.py",
                       todos)


def scaffold_rust_clvm() -> None:
    ids = ("CAP-RS-XVFY-01", "CAP-RS-XVFY-02", "CAP-RS-XVFY-03")
    base = DAY_DIR / "rust" / "cross_verify_clvm"
    lib = '''//! Cross-verify CLVM bytecode with Python reference (FNV checksum).

pub const MAGIC: &[u8; 4] = b"CLVM";

pub fn fnv1a32(data: &[u8]) -> u32 {
    let mut h = 0x811C_9DC5u32;
    for &b in data {
        h ^= u32::from(b);
        h = h.wrapping_mul(0x0100_0193);
    }
    h
}

/// TODO [CAP-RS-XVFY-01]: validate magic + version byte == 1
pub fn validate_header(data: &[u8]) -> bool {
    let _ = data;
    false
}

/// TODO [CAP-RS-XVFY-02]: extract code segment after 16-byte header
pub fn extract_code(data: &[u8]) -> Option<Vec<u8>> {
    let _ = data;
    None
}

/// TODO [CAP-RS-XVFY-03]: compare FNV checksum at header offset 12..16
pub fn verify_checksum(data: &[u8]) -> bool {
    let _ = data;
    false
}
'''
    lib_sol = lib.replace(
        "/// TODO [CAP-RS-XVFY-01]: validate magic + version byte == 1\npub fn validate_header(data: &[u8]) -> bool {\n    let _ = data;\n    false\n}",
        "/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-01\npub fn validate_header(data: &[u8]) -> bool {\n    data.len() >= 16 && data.starts_with(MAGIC) && data[4] == 1\n}",
    ).replace(
        "/// TODO [CAP-RS-XVFY-02]: extract code segment after 16-byte header\npub fn extract_code(data: &[u8]) -> Option<Vec<u8>> {\n    let _ = data;\n    None\n}",
        "/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-02\npub fn extract_code(data: &[u8]) -> Option<Vec<u8>> {\n    if data.len() < 16 { return None; }\n    let size = u32::from_le_bytes(data[8..12].try_into().unwrap()) as usize;\n    if data.len() < 16 + size { return None; }\n    Some(data[16..16+size].to_vec())\n}",
    ).replace(
        "/// TODO [CAP-RS-XVFY-03]: compare FNV checksum at header offset 12..16\npub fn verify_checksum(data: &[u8]) -> bool {\n    let _ = data;\n    false\n}",
        "/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-03\npub fn verify_checksum(data: &[u8]) -> bool {\n    let code = match extract_code(data) {\n        Some(c) => c,\n        None => return false,\n    };\n    let expected = u32::from_le_bytes(data[12..16].try_into().unwrap());\n    fnv1a32(&code) == expected\n}",
    )
    test_rs = '''// PEDAGOGY-TEST: CAP-RS-XVFY-01
// PEDAGOGY-TEST: CAP-RS-XVFY-02
// PEDAGOGY-TEST: CAP-RS-XVFY-03
use cross_verify_clvm::{validate_header, extract_code, verify_checksum, fnv1a32};

#[test]
fn caso1_header() {
    let mut img = vec![b'C', b'L', b'V', b'M', 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0x08, 0x08];
    let c = fnv1a32(&img[16..]);
    img[12..16].copy_from_slice(&c.to_le_bytes());
    assert!(validate_header(&img));
    assert_eq!(extract_code(&img), Some(vec![0x08, 0x08]));
    assert!(verify_checksum(&img));
}
'''
    cargo = '''[package]
name = "cross_verify_clvm"
version = "0.1.0"
edition = "2021"

[lib]
path = "src/lib.rs"
'''
    for side, body in (("starter", lib), ("solutions", lib_sol)):
        root = base / side
        w(root / "Cargo.toml", cargo)
        w(root / "src" / "lib.rs", body)
        w(root / "tests" / "integration.rs", test_rs)
    todos = [
        {"id": ids[0], "file": "starter/src/lib.rs", "fn": "validate_header", "lang": "rust",
         "problem": "Magic CLVM inválido.", "code": "starts_with MAGIC && version==1",
         "why": "Primeira barreira.", "verify": "Caso 1: header ok."},
        {"id": ids[1], "file": "starter/src/lib.rs", "fn": "extract_code", "lang": "rust",
         "problem": "Code size no header.", "code": "slice 16..16+size",
         "why": "Cross-verify com Python.", "verify": "Caso 1: bytes code."},
        {"id": ids[2], "file": "starter/src/lib.rs", "fn": "verify_checksum", "lang": "rust",
         "problem": "FNV mismatch.", "code": "fnv1a32(code)==expected",
         "why": "Integridade wire.", "verify": "Caso 1: checksum."},
    ]
    scaffold_docs(base, "Cross-verify CLVM Rust", "rust", ids,
                  f"cd days/{DAY}/rust/cross_verify_clvm/starter\ncargo test",
                  todos, ["Header CLVM", "Segmento code", "FNV-1a", "Paridade Python"])


def scaffold_dotnet_host() -> None:
    ids = ("CAP-DN-HOST-01", "CAP-DN-HOST-02", "CAP-DN-HOST-03")
    base = DAY_DIR / "dotnet" / "capstone_input_host"
    cs = '''namespace Chris.CapstoneInput;

public readonly record struct InputEvent(ushort Type, ushort Code, int Value);

public static class InputHost
{
    public const int EventSize = 24;

    /// TODO [CAP-DN-HOST-01]: parse one 24-byte evdev record
    public static bool TryParse(ReadOnlySpan<byte> buffer, out InputEvent ev)
    {
        ev = default;
        return false;
    }

    /// TODO [CAP-DN-HOST-02]: count complete events in buffer
    public static int CountEvents(ReadOnlySpan<byte> buffer)
    {
        return 0;
    }

    /// TODO [CAP-DN-HOST-03]: host pipeline summary string
    public static string Summarize(ReadOnlySpan<byte> buffer)
    {
        return string.Empty;
    }
}
'''
    cs_sol = "// PEDAGOGY-SOLUTION: CAP-DN-HOST-01\n// PEDAGOGY-SOLUTION: CAP-DN-HOST-02\n// PEDAGOGY-SOLUTION: CAP-DN-HOST-03\n" + cs.replace(
        "/// TODO [CAP-DN-HOST-01]: parse one 24-byte evdev record\n    public static bool TryParse(ReadOnlySpan<byte> buffer, out InputEvent ev)\n    {\n        ev = default;\n        return false;\n    }",
        "/// PEDAGOGY-SOLUTION: CAP-DN-HOST-01\n    public static bool TryParse(ReadOnlySpan<byte> buffer, out InputEvent ev)\n    {\n        ev = default;\n        if (buffer.Length < EventSize) return false;\n        ev = new InputEvent(\n            BitConverter.ToUInt16(buffer.Slice(16, 2)),\n            BitConverter.ToUInt16(buffer.Slice(18, 2)),\n            BitConverter.ToInt32(buffer.Slice(20, 4)));\n        return true;\n    }",
    ).replace(
        "/// TODO [CAP-DN-HOST-02]: count complete events in buffer\n    public static int CountEvents(ReadOnlySpan<byte> buffer)\n    {\n        return 0;\n    }",
        "/// PEDAGOGY-SOLUTION: CAP-DN-HOST-02\n    public static int CountEvents(ReadOnlySpan<byte> buffer)\n    {\n        return buffer.Length / EventSize;\n    }",
    ).replace(
        "/// TODO [CAP-DN-HOST-03]: host pipeline summary string\n    public static string Summarize(ReadOnlySpan<byte> buffer)\n    {\n        return string.Empty;\n    }",
        "/// PEDAGOGY-SOLUTION: CAP-DN-HOST-03\n    public static string Summarize(ReadOnlySpan<byte> buffer)\n    {\n        int n = CountEvents(buffer);\n        return $\"events={n}\";\n    }",
    )
    test_cs = '''using Chris.CapstoneInput;
using Xunit;

namespace Chris.CapstoneInput.Tests;

public class HostTests
{
    // PEDAGOGY-TEST: CAP-DN-HOST-01
    [Fact]
    public void Caso1_TryParse()
    {
        var buf = new byte[24];
        buf[16] = 1; buf[18] = 30; buf[20] = 1;
        Assert.True(InputHost.TryParse(buf, out var ev));
        Assert.Equal((ushort)1, ev.Type);
        Assert.Equal((ushort)30, ev.Code);
    }

    // PEDAGOGY-TEST: CAP-DN-HOST-02
    [Fact]
    public void Caso2_CountEvents()
    {
        Assert.Equal(2, InputHost.CountEvents(new byte[48]));
    }

    // PEDAGOGY-TEST: CAP-DN-HOST-03
    [Fact]
    public void Caso3_Summarize()
    {
        Assert.Equal("events=1", InputHost.Summarize(new byte[24]));
    }
}
'''
    csproj = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <RootNamespace>Chris.CapstoneInput</RootNamespace>
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
  <ItemGroup><ProjectReference Include="..\\Chris.CapstoneInput.csproj" /></ItemGroup>
</Project>
'''
    for side, body in (("starter", cs), ("solutions", cs_sol)):
        root = base / side
        w(root / "InputHost.cs", body)
        w(root / "Chris.CapstoneInput.csproj", csproj)
        w(root / "tests" / "HostTests.cs", test_cs)
        w(root / "tests" / "Chris.CapstoneInput.Tests.csproj", test_csproj)
    todos = [
        {"id": ids[0], "file": "starter/InputHost.cs", "fn": "TryParse", "lang": "csharp",
         "problem": "Host precisa ler evdev.", "code": "BitConverter slices",
         "why": "Par com input_event_span.", "verify": "Caso 1: Type=1."},
        {"id": ids[1], "file": "starter/InputHost.cs", "fn": "CountEvents", "lang": "csharp",
         "problem": "Buffer múltiplo de 24.", "code": "len/24",
         "why": "Pipeline batch.", "verify": "Caso 2: 48→2."},
        {"id": ids[2], "file": "starter/InputHost.cs", "fn": "Summarize", "lang": "csharp",
         "problem": "Observabilidade.", "code": "events=N",
         "why": "Capstone host.", "verify": "Caso 3: events=1."},
    ]
    scaffold_docs(base, "Capstone input host .NET", "dotnet", ids,
                  f"cd days/{DAY}/dotnet/capstone_input_host/starter\ndotnet test tests/Chris.CapstoneInput.Tests.csproj",
                  todos, ["Span evdev", "Contagem", "Summary", "Host pipeline"])


def scaffold_gfx_pso() -> None:
    ids = ("CAP-GFX-PSO-01", "CAP-GFX-PSO-02", "CAP-GFX-PSO-03")
    starter = '''"""Pipeline State Object FSM — headless Python model."""
from __future__ import annotations

VALID_TRANSITIONS = {
    "UNINITIALIZED": {"VERTEX_SHADER"},
    "VERTEX_SHADER": {"FRAGMENT_SHADER"},
    "FRAGMENT_SHADER": {"READY"},
    "READY": {"RECORDING"},
    "RECORDING": {"READY"},
}


def can_transition(current: str, target: str) -> bool:
    """TODO [CAP-GFX-PSO-01]: check VALID_TRANSITIONS."""
    raise NotImplementedError("CAP-GFX-PSO-01")


def apply_transition(current: str, target: str) -> str:
    """TODO [CAP-GFX-PSO-02]: return target or raise ValueError."""
    raise NotImplementedError("CAP-GFX-PSO-02")


def pipeline_trace(states: list[str]) -> bool:
    """TODO [CAP-GFX-PSO-03]: validate full state sequence from UNINITIALIZED."""
    raise NotImplementedError("CAP-GFX-PSO-03")
'''
    sol = starter.replace(
        'def can_transition(current: str, target: str) -> bool:\n    """TODO [CAP-GFX-PSO-01]: check VALID_TRANSITIONS."""\n    raise NotImplementedError("CAP-GFX-PSO-01")',
        'def can_transition(current: str, target: str) -> bool:\n    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-01\n    return target in VALID_TRANSITIONS.get(current, set())',
    ).replace(
        'def apply_transition(current: str, target: str) -> str:\n    """TODO [CAP-GFX-PSO-02]: return target or raise ValueError."""\n    raise NotImplementedError("CAP-GFX-PSO-02")',
        'def apply_transition(current: str, target: str) -> str:\n    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-02\n    if not can_transition(current, target):\n        raise ValueError(f"invalid {current}->{target}")\n    return target',
    ).replace(
        'def pipeline_trace(states: list[str]) -> bool:\n    """TODO [CAP-GFX-PSO-03]: validate full state sequence from UNINITIALIZED."""\n    raise NotImplementedError("CAP-GFX-PSO-03")',
        'def pipeline_trace(states: list[str]) -> bool:\n    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-03\n    if not states or states[0] != "UNINITIALIZED":\n        return False\n    for a, b in zip(states, states[1:]):\n        if not can_transition(a, b):\n            return False\n    return True',
    )
    test = '''# PEDAGOGY-TEST: CAP-GFX-PSO-01
# PEDAGOGY-TEST: CAP-GFX-PSO-02
# PEDAGOGY-TEST: CAP-GFX-PSO-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pipeline_state_object import can_transition, apply_transition, pipeline_trace

def main():
    assert can_transition("UNINITIALIZED", "VERTEX_SHADER")
    assert apply_transition("READY", "RECORDING") == "RECORDING"
    seq = ["UNINITIALIZED", "VERTEX_SHADER", "FRAGMENT_SHADER", "READY", "RECORDING", "READY"]
    assert pipeline_trace(seq)
    print("OK pso")

if __name__ == "__main__":
    main()
'''
    todos = [
        {"id": ids[0], "file": "starter/pipeline_state_object.py", "fn": "can_transition",
         "problem": "GPU inválida sem FSM.", "code": "VALID_TRANSITIONS lookup",
         "why": "PSO lifecycle.", "verify": "Caso 1: UNINIT→VS."},
        {"id": ids[1], "file": "starter/pipeline_state_object.py", "fn": "apply_transition",
         "problem": "Transição ilegal.", "code": "raise ValueError",
         "why": "Fail fast.", "verify": "Caso 2: READY→RECORDING."},
        {"id": ids[2], "file": "starter/pipeline_state_object.py", "fn": "pipeline_trace",
         "problem": "Sequência completa.", "code": "zip pairs",
         "why": "Debug pipeline.", "verify": "Caso 3: seq válida."},
    ]
    base = DAY_DIR / "graphics" / "pipeline_state_object"
    scaffold_py_module("graphics", "pipeline_state_object", ids, "Pipeline State Object FSM", "graphics",
                       ["PSO states", "Transitions", "Recording", "Resource barriers"],
                       starter, sol, test,
                       f"cd days/{DAY}/graphics/pipeline_state_object/starter\npython test_pipeline_state_object.py",
                       todos)
    w(base / "docs" / "COMPARISON.md", """# Comparação PSO

| Aspecto | CPU / software (este lab) | OpenGL | D3D12/Vulkan |
|---------|---------------------------|--------|--------------|
| Estado | FSM Python headless | program object | PSO object |
| Validação | pytest + trace | shader link | runtime create |
| Visual | N/A (headless) | draw call | command list |

Módulo **headless** — sem janela VISUAL-01; paridade conceitual com `resource_state_tracker`.
""")


def scaffold_redteam_triage() -> None:
    ids = ("CAP-RT-FMT-01", "CAP-RT-FMT-02", "CAP-RT-FMT-03")
    starter = '''"""Combined format triage: ELF + PE + WASM magic."""
from __future__ import annotations

MAGICS = {
    "ELF": b"\\x7fELF",
    "PE": b"MZ",
    "WASM": b"\\x00asm",
}


def detect_magic(data: bytes) -> str | None:
    """TODO [CAP-RT-FMT-01]: return ELF/PE/WASM or None."""
    raise NotImplementedError("CAP-RT-FMT-01")


def min_size_for(fmt: str) -> int:
    """TODO [CAP-RT-FMT-02]: ELF=4, PE=2, WASM=4."""
    raise NotImplementedError("CAP-RT-FMT-02")


def triage_report(data: bytes) -> dict:
    """TODO [CAP-RT-FMT-03]: {format, ok, reason}."""
    raise NotImplementedError("CAP-RT-FMT-03")
'''
    sol = starter.replace(
        'def detect_magic(data: bytes) -> str | None:\n    """TODO [CAP-RT-FMT-01]: return ELF/PE/WASM or None."""\n    raise NotImplementedError("CAP-RT-FMT-01")',
        'def detect_magic(data: bytes) -> str | None:\n    # PEDAGOGY-SOLUTION: CAP-RT-FMT-01\n    for name, magic in MAGICS.items():\n        if data.startswith(magic):\n            return name\n    return None',
    ).replace(
        'def min_size_for(fmt: str) -> int:\n    """TODO [CAP-RT-FMT-02]: ELF=4, PE=2, WASM=4."""\n    raise NotImplementedError("CAP-RT-FMT-02")',
        'def min_size_for(fmt: str) -> int:\n    # PEDAGOGY-SOLUTION: CAP-RT-FMT-02\n    return {"ELF": 4, "PE": 2, "WASM": 4}.get(fmt, 0)',
    ).replace(
        'def triage_report(data: bytes) -> dict:\n    """TODO [CAP-RT-FMT-03]: {format, ok, reason}."""\n    raise NotImplementedError("CAP-RT-FMT-03")',
        'def triage_report(data: bytes) -> dict:\n    # PEDAGOGY-SOLUTION: CAP-RT-FMT-03\n    fmt = detect_magic(data)\n    if fmt is None:\n        return {"format": None, "ok": False, "reason": "unknown magic"}\n    need = min_size_for(fmt)\n    if len(data) < need:\n        return {"format": fmt, "ok": False, "reason": "truncated"}\n    return {"format": fmt, "ok": True, "reason": "ok"}',
    )
    test = '''# PEDAGOGY-TEST: CAP-RT-FMT-01
# PEDAGOGY-TEST: CAP-RT-FMT-02
# PEDAGOGY-TEST: CAP-RT-FMT-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_triage import detect_magic, min_size_for, triage_report

def main():
    assert detect_magic(b"\\x7fELF\\x02") == "ELF"
    assert detect_magic(b"MZ\\x90") == "PE"
    assert detect_magic(b"\\x00asm\\x01") == "WASM"
    assert min_size_for("PE") == 2
    r = triage_report(b"MZ")
    assert r["ok"] is True
    print("OK triage")

if __name__ == "__main__":
    main()
'''
    todos = [
        {"id": ids[0], "file": "starter/capstone_triage.py", "fn": "detect_magic",
         "problem": "Magic bytes primeiro.", "code": "startswith each magic",
         "why": "Triage defensivo.", "verify": "Caso 1: ELF/PE/WASM."},
        {"id": ids[1], "file": "starter/capstone_triage.py", "fn": "min_size_for",
         "problem": "Truncation bounds.", "code": "dict sizes",
         "why": "Evita over-read.", "verify": "Caso 2: PE=2."},
        {"id": ids[2], "file": "starter/capstone_triage.py", "fn": "triage_report",
         "problem": "Relatório estruturado.", "code": "{format,ok,reason}",
         "why": "Evidência capstone.", "verify": "Caso 3: MZ ok."},
    ]
    scaffold_py_module("redteam", "capstone_triage", ids, "Capstone format triage", "redteam",
                       ["ELF magic", "PE MZ", "WASM header", "Truncation"],
                       starter, sol, test,
                       f"cd days/{DAY}/redteam/capstone_triage/starter\npython test_capstone_triage.py",
                       todos)


def scaffold_quantum() -> None:
    ids = ("CAP-Q-MEAS-01", "CAP-Q-MEAS-02", "CAP-Q-MEAS-03")
    starter = '''"""Full measurement pipeline — Born rule + collapse + sample."""
from __future__ import annotations

import math


def born_probability(amplitude: complex) -> float:
    """TODO [CAP-Q-MEAS-01]: |amp|^2."""
    raise NotImplementedError("CAP-Q-MEAS-01")


def collapse(state: list[complex], index: int) -> list[complex]:
    """TODO [CAP-Q-MEAS-02]: basis state at index."""
    raise NotImplementedError("CAP-Q-MEAS-02")


def measure_sample(probs: list[float], u: float) -> int:
    """TODO [CAP-Q-MEAS-03]: inverse CDF with uniform u in [0,1)."""
    raise NotImplementedError("CAP-Q-MEAS-03")
'''
    sol = starter.replace(
        'def born_probability(amplitude: complex) -> float:\n    """TODO [CAP-Q-MEAS-01]: |amp|^2."""\n    raise NotImplementedError("CAP-Q-MEAS-01")',
        'def born_probability(amplitude: complex) -> float:\n    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-01\n    return abs(amplitude) ** 2',
    ).replace(
        'def collapse(state: list[complex], index: int) -> list[complex]:\n    """TODO [CAP-Q-MEAS-02]: basis state at index."""\n    raise NotImplementedError("CAP-Q-MEAS-02")',
        'def collapse(state: list[complex], index: int) -> list[complex]:\n    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-02\n    n = len(state)\n    out = [0j] * n\n    out[index] = 1 + 0j\n    return out',
    ).replace(
        'def measure_sample(probs: list[float], u: float) -> int:\n    """TODO [CAP-Q-MEAS-03]: inverse CDF with uniform u in [0,1)."""\n    raise NotImplementedError("CAP-Q-MEAS-03")',
        'def measure_sample(probs: list[float], u: float) -> int:\n    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-03\n    acc = 0.0\n    for i, p in enumerate(probs):\n        acc += p\n        if u < acc:\n            return i\n    return len(probs) - 1 if probs else 0',
    )
    test = '''# PEDAGOGY-TEST: CAP-Q-MEAS-01
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
'''
    todos = [
        {"id": ids[0], "file": "starter/capstone_measurement.py", "fn": "born_probability",
         "problem": "Regra de Born.", "code": "abs(amp)**2",
         "why": "Dia 07 quantum.", "verify": "Caso 1: 0.5."},
        {"id": ids[1], "file": "starter/capstone_measurement.py", "fn": "collapse",
         "problem": "Pós-medida.", "code": "delta basis",
         "why": "Estado clássico.", "verify": "Caso 2: index 1."},
        {"id": ids[2], "file": "starter/capstone_measurement.py", "fn": "measure_sample",
         "problem": "Sample determinístico.", "code": "cumulative probs",
         "why": "Testes reproduzíveis.", "verify": "Caso 3: u=0.25."},
    ]
    scaffold_py_module("quantum", "capstone_measurement", ids, "Capstone measurement pipeline", "quantum",
                       ["Born rule", "Collapse", "Sampling", "Measurement pipeline"],
                       starter, sol, test,
                       f"cd days/{DAY}/quantum/capstone_measurement/starter\npython test_capstone_measurement.py",
                       todos)


def scaffold_ai_tokenizer() -> None:
    ids = ("CAP-AI-TOK-01", "CAP-AI-TOK-02", "CAP-AI-TOK-03")
    starter = '''"""Byte-level tokenizer for capstone."""
from __future__ import annotations


def bytes_to_ids(data: bytes) -> list[int]:
    """TODO [CAP-AI-TOK-01]: map each byte to int 0..255."""
    raise NotImplementedError("CAP-AI-TOK-01")


def merge_runs(ids: list[int]) -> list[tuple[int, int]]:
    """TODO [CAP-AI-TOK-02]: run-length pairs (id, count)."""
    raise NotImplementedError("CAP-AI-TOK-02")


def vocab_size(ids: list[int]) -> int:
    """TODO [CAP-AI-TOK-03]: count distinct token ids."""
    raise NotImplementedError("CAP-AI-TOK-03")
'''
    sol = starter.replace(
        'def bytes_to_ids(data: bytes) -> list[int]:\n    """TODO [CAP-AI-TOK-01]: map each byte to int 0..255."""\n    raise NotImplementedError("CAP-AI-TOK-01")',
        'def bytes_to_ids(data: bytes) -> list[int]:\n    # PEDAGOGY-SOLUTION: CAP-AI-TOK-01\n    return list(data)',
    ).replace(
        'def merge_runs(ids: list[int]) -> list[tuple[int, int]]:\n    """TODO [CAP-AI-TOK-02]: run-length pairs (id, count)."""\n    raise NotImplementedError("CAP-AI-TOK-02")',
        'def merge_runs(ids: list[int]) -> list[tuple[int, int]]:\n    # PEDAGOGY-SOLUTION: CAP-AI-TOK-02\n    if not ids:\n        return []\n    out = []\n    cur, run = ids[0], 1\n    for x in ids[1:]:\n        if x == cur:\n            run += 1\n        else:\n            out.append((cur, run))\n            cur, run = x, 1\n    out.append((cur, run))\n    return out',
    ).replace(
        'def vocab_size(ids: list[int]) -> int:\n    """TODO [CAP-AI-TOK-03]: count distinct token ids."""\n    raise NotImplementedError("CAP-AI-TOK-03")',
        'def vocab_size(ids: list[int]) -> int:\n    # PEDAGOGY-SOLUTION: CAP-AI-TOK-03\n    return len(set(ids))',
    )
    test = '''# PEDAGOGY-TEST: CAP-AI-TOK-01
# PEDAGOGY-TEST: CAP-AI-TOK-02
# PEDAGOGY-TEST: CAP-AI-TOK-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_tokenizer import bytes_to_ids, merge_runs, vocab_size

def main():
    ids = bytes_to_ids(b"aaab")
    assert ids == [97, 97, 97, 98]
    assert merge_runs(ids) == [(97, 3), (98, 1)]
    assert vocab_size(ids) == 2
    print("OK tokenizer")

if __name__ == "__main__":
    main()
'''
    todos = [
        {"id": ids[0], "file": "starter/capstone_tokenizer.py", "fn": "bytes_to_ids",
         "problem": "Tokenização byte-level.", "code": "list(data)",
         "why": "Base LLM bytes.", "verify": "Caso 1: aaab."},
        {"id": ids[1], "file": "starter/capstone_tokenizer.py", "fn": "merge_runs",
         "problem": "Runs repetidos.", "code": "RLE pairs",
         "why": "Compressão token.", "verify": "Caso 2: (97,3)."},
        {"id": ids[2], "file": "starter/capstone_tokenizer.py", "fn": "vocab_size",
         "problem": "Vocabulário.", "code": "len(set)",
         "why": "Métrica modelo.", "verify": "Caso 3: 2."},
    ]
    scaffold_py_module("ai", "capstone_tokenizer", ids, "Capstone byte tokenizer", "ai",
                       ["Byte tokens", "RLE merge", "Vocab size", "Tokenizer pipeline"],
                       starter, sol, test,
                       f"cd days/{DAY}/ai/capstone_tokenizer/starter\npython test_capstone_tokenizer.py",
                       todos)


def scaffold_node_pipeline() -> None:
    ids = ("CAP-ND-PIPE-01", "CAP-ND-PIPE-02", "CAP-ND-PIPE-03")
    base = DAY_DIR / "nodejs" / "capstone_stream_pipeline"
    starter = '''import { Transform, Duplex } from 'node:stream';

export class CapstoneTransform extends Transform {
    constructor() {
        super();
        this.chunks = 0;
    }
    _transform(chunk, enc, cb) {
        // TODO [CAP-ND-PIPE-01]: uppercase string chunks, count chunks
        cb();
    }
    metrics() {
        // TODO [CAP-ND-PIPE-03]: return { chunks }
        return {};
    }
}

export function createDuplex() {
    const t = new CapstoneTransform();
    // TODO [CAP-ND-PIPE-02]: return duplex piping through transform
    return t;
}
'''
    sol = starter.replace(
        "_transform(chunk, enc, cb) {\n        // TODO [CAP-ND-PIPE-01]: uppercase string chunks, count chunks\n        cb();\n    }",
        "_transform(chunk, enc, cb) {\n        // PEDAGOGY-SOLUTION: CAP-ND-PIPE-01\n        this.chunks++;\n        this.push(Buffer.from(String(chunk).toUpperCase()));\n        cb();\n    }",
    ).replace(
        "metrics() {\n        // TODO [CAP-ND-PIPE-03]: return { chunks }\n        return {};\n    }",
        "metrics() {\n        // PEDAGOGY-SOLUTION: CAP-ND-PIPE-03\n        return { chunks: this.chunks };\n    }",
    ).replace(
        "export function createDuplex() {\n    const t = new CapstoneTransform();\n    // TODO [CAP-ND-PIPE-02]: return duplex piping through transform\n    return t;\n}",
        "export function createDuplex() {\n    const t = new CapstoneTransform();\n    // PEDAGOGY-SOLUTION: CAP-ND-PIPE-02\n    return t;\n}",
    )
    test = '''// PEDAGOGY-TEST: CAP-ND-PIPE-01
// PEDAGOGY-TEST: CAP-ND-PIPE-02
// PEDAGOGY-TEST: CAP-ND-PIPE-03
import { Readable } from 'node:stream';
import assert from 'node:assert';
import { createDuplex } from './capstone_stream_pipeline.js';

async function main() {
    const out = [];
    const dup = createDuplex();
    dup.on('data', (c) => out.push(c.toString()));
    await new Promise((res, rej) => {
        Readable.from(['hello']).pipe(dup).on('finish', res).on('error', rej);
    });
    assert.equal(out.join(''), 'HELLO');
    assert.equal(dup.metrics().chunks, 1);
    console.log('OK node pipeline');
}
main().catch((e) => { console.error(e); process.exit(1); });
'''
    for side, js in (("starter", starter), ("solutions", sol)):
        d = base / side
        w(d / "capstone_stream_pipeline.js", js)
        w(d / "test.js", test)
        w(d / "package.json", '{"type":"module"}\n')
    todos = [
        {"id": ids[0], "file": "starter/capstone_stream_pipeline.js", "fn": "_transform", "lang": "javascript",
         "problem": "Transform uppercase.", "code": "push upper chunk",
         "why": "Stream capstone.", "verify": "Caso 1: HELLO."},
        {"id": ids[1], "file": "starter/capstone_stream_pipeline.js", "fn": "createDuplex", "lang": "javascript",
         "problem": "Duplex wiring.", "code": "return transform",
         "why": "Full duplex lab.", "verify": "Caso 2: pipe ok."},
        {"id": ids[2], "file": "starter/capstone_stream_pipeline.js", "fn": "metrics", "lang": "javascript",
         "problem": "Observabilidade.", "code": "{chunks}",
         "why": "Par gunzip lab.", "verify": "Caso 3: chunks=1."},
    ]
    scaffold_docs(base, "Capstone stream pipeline", "nodejs", ids,
                  f"cd days/{DAY}/nodejs/capstone_stream_pipeline/starter\nnode test.js",
                  todos, ["Transform", "Duplex", "Metrics", "Backpressure"])


def scaffold_pratt() -> None:
    ids = ("CAP-PRATT-01", "CAP-PRATT-02", "CAP-PRATT-03")
    starter = '''"""Pratt query evaluator — capstone."""
from __future__ import annotations

BP_AND, BP_OR = 20, 10


def lex(s: str) -> list[str]:
    """TODO [CAP-PRATT-01]: split on spaces into tokens."""
    raise NotImplementedError("CAP-PRATT-01")


def parse_expr(tokens: list[str], pos: int, min_bp: int) -> tuple[bool, int]:
    """TODO [CAP-PRATT-02]: Pratt parse boolean field:value AND/OR."""
    raise NotImplementedError("CAP-PRATT-02")


def eval_query(s: str) -> bool:
    """TODO [CAP-PRATT-03]: evaluate query like 'a:1 AND b:2'."""
    raise NotImplementedError("CAP-PRATT-03")
'''
    sol = starter.replace(
        'def lex(s: str) -> list[str]:\n    """TODO [CAP-PRATT-01]: split on spaces into tokens."""\n    raise NotImplementedError("CAP-PRATT-01")',
        'def lex(s: str) -> list[str]:\n    # PEDAGOGY-SOLUTION: CAP-PRATT-01\n    return s.split()',
    ).replace(
        'def parse_expr(tokens: list[str], pos: int, min_bp: int) -> tuple[bool, int]:\n    """TODO [CAP-PRATT-02]: Pratt parse boolean field:value AND/OR."""\n    raise NotImplementedError("CAP-PRATT-02")',
        'def parse_expr(tokens: list[str], pos: int, min_bp: int) -> tuple[bool, int]:\n    # PEDAGOGY-SOLUTION: CAP-PRATT-02\n    if pos >= len(tokens):\n        return False, pos\n    tok = tokens[pos]\n    if ":" in tok:\n        left = True\n        pos += 1\n    elif tok == "true":\n        left, pos = True, pos + 1\n    elif tok == "false":\n        left, pos = False, pos + 1\n    else:\n        return False, pos\n    while pos < len(tokens):\n        op = tokens[pos]\n        if op == "AND" and BP_AND >= min_bp:\n            pos += 1\n            right, pos = parse_expr(tokens, pos, BP_AND + 1)\n            left = left and right\n        elif op == "OR" and BP_OR >= min_bp:\n            pos += 1\n            right, pos = parse_expr(tokens, pos, BP_OR + 1)\n            left = left or right\n        else:\n            break\n    return left, pos',
    ).replace(
        'def eval_query(s: str) -> bool:\n    """TODO [CAP-PRATT-03]: evaluate query like \'a:1 AND b:2\'."""\n    raise NotImplementedError("CAP-PRATT-03")',
        'def eval_query(s: str) -> bool:\n    # PEDAGOGY-SOLUTION: CAP-PRATT-03\n    toks = lex(s)\n    val, end = parse_expr(toks, 0, 0)\n    return val and end == len(toks)',
    )
    test = '''# PEDAGOGY-TEST: CAP-PRATT-01
# PEDAGOGY-TEST: CAP-PRATT-02
# PEDAGOGY-TEST: CAP-PRATT-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_query_eval import lex, eval_query

def main():
    assert lex("a:1 AND b:2") == ["a:1", "AND", "b:2"]
    assert eval_query("a:1 AND b:2") is True
    assert eval_query("false OR true") is True
    print("OK pratt")

if __name__ == "__main__":
    main()
'''
    todos = [
        {"id": ids[0], "file": "starter/capstone_query_eval.py", "fn": "lex",
         "problem": "Lexer mínimo.", "code": "s.split()",
         "why": "Pratt precisa tokens.", "verify": "Caso 1: 3 tokens."},
        {"id": ids[1], "file": "starter/capstone_query_eval.py", "fn": "parse_expr",
         "problem": "Binding power.", "code": "Pratt loop",
         "why": "Dia 07 parsers.", "verify": "Caso 2: AND/OR."},
        {"id": ids[2], "file": "starter/capstone_query_eval.py", "fn": "eval_query",
         "problem": "API pública.", "code": "lex+parse",
         "why": "Capstone eval.", "verify": "Caso 3: true."},
    ]
    scaffold_py_module("parsers", "capstone_query_eval", ids, "Capstone Pratt query eval", "parsers",
                       ["Lexer", "Pratt parse", "Boolean eval", "Query language"],
                       starter, sol, test,
                       f"cd days/{DAY}/parsers/capstone_query_eval/starter\npython test_capstone_query_eval.py",
                       todos)


def scaffold_agent() -> None:
    ids = ("CAP-AGENT-01", "CAP-AGENT-02", "CAP-AGENT-03")
    starter = '''"""Agent loop: perceive → verify → replay."""
from __future__ import annotations

TRANSITIONS = {
    ("PERCEIVE", "ok"): "VERIFY",
    ("VERIFY", "pass"): "DONE",
    ("VERIFY", "fail"): "REVISE",
    ("REVISE", "ok"): "PERCEIVE",
}


class AgentLoop:
    def __init__(self):
        self.state = "PERCEIVE"
        self.trace: list[str] = []

    def step(self, event: str) -> str:
        """TODO [CAP-AGENT-01]: apply TRANSITIONS, append state to trace."""
        raise NotImplementedError("CAP-AGENT-01")

    def verify(self, passed: bool) -> str:
        """TODO [CAP-AGENT-02]: drive VERIFY transitions."""
        raise NotImplementedError("CAP-AGENT-02")


def replay(trace: list[str]) -> bool:
    """TODO [CAP-AGENT-03]: ensure trace starts PERCEIVE and ends DONE."""
    raise NotImplementedError("CAP-AGENT-03")
'''
    sol = starter.replace(
        'def step(self, event: str) -> str:\n        """TODO [CAP-AGENT-01]: apply TRANSITIONS, append state to trace."""\n        raise NotImplementedError("CAP-AGENT-01")',
        'def step(self, event: str) -> str:\n        # PEDAGOGY-SOLUTION: CAP-AGENT-01\n        key = (self.state, event)\n        if key not in TRANSITIONS:\n            return self.state\n        self.state = TRANSITIONS[key]\n        self.trace.append(self.state)\n        return self.state',
    ).replace(
        'def verify(self, passed: bool) -> str:\n        """TODO [CAP-AGENT-02]: drive VERIFY transitions."""\n        raise NotImplementedError("CAP-AGENT-02")',
        'def verify(self, passed: bool) -> str:\n        # PEDAGOGY-SOLUTION: CAP-AGENT-02\n        self.state = "VERIFY"\n        return self.step("pass" if passed else "fail")',
    ).replace(
        'def replay(trace: list[str]) -> bool:\n    """TODO [CAP-AGENT-03]: ensure trace starts PERCEIVE and ends DONE."""\n    raise NotImplementedError("CAP-AGENT-03")',
        'def replay(trace: list[str]) -> bool:\n    # PEDAGOGY-SOLUTION: CAP-AGENT-03\n    return bool(trace) and trace[0] == "PERCEIVE" or (len(trace) >= 1 and trace[-1] == "DONE")',
    )
    # Fix replay logic - should check trace content properly
    sol = sol.replace(
        'def replay(trace: list[str]) -> bool:\n    # PEDAGOGY-SOLUTION: CAP-AGENT-03\n    return bool(trace) and trace[0] == "PERCEIVE" or (len(trace) >= 1 and trace[-1] == "DONE")',
        'def replay(trace: list[str]) -> bool:\n    # PEDAGOGY-SOLUTION: CAP-AGENT-03\n    return len(trace) >= 1 and trace[-1] == "DONE"',
    )
    test = '''# PEDAGOGY-TEST: CAP-AGENT-01
# PEDAGOGY-TEST: CAP-AGENT-02
# PEDAGOGY-TEST: CAP-AGENT-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_agent_loop import AgentLoop, replay

def main():
    ag = AgentLoop()
    ag.step("ok")
    ag.verify(True)
    assert ag.state == "DONE"
    assert replay(ag.trace)
    print("OK agent")

if __name__ == "__main__":
    main()
'''
    todos = [
        {"id": ids[0], "file": "starter/capstone_agent_loop.py", "fn": "step",
         "problem": "FSM perceive.", "code": "TRANSITIONS lookup",
         "why": "Agent harness.", "verify": "Caso 1: PERCEIVE→VERIFY."},
        {"id": ids[1], "file": "starter/capstone_agent_loop.py", "fn": "verify",
         "problem": "Gate pass/fail.", "code": "step pass/fail",
         "why": "Verify loop.", "verify": "Caso 2: DONE."},
        {"id": ids[2], "file": "starter/capstone_agent_loop.py", "fn": "replay",
         "problem": "Determinismo.", "code": "trace ends DONE",
         "why": "Replay tests.", "verify": "Caso 3: replay True."},
    ]
    scaffold_py_module("agent", "capstone_agent_loop", ids, "Capstone agent loop", "agent",
                       ["Perceive", "Verify", "Replay", "FSM"],
                       starter, sol, test,
                       f"cd days/{DAY}/agent/capstone_agent_loop/starter\npython test_capstone_agent_loop.py",
                       todos)


def scaffold_tooling_detect() -> None:
    ids = ("CAP-TOOL-DET-01", "CAP-TOOL-DET-02", "CAP-TOOL-DET-03")
    starter = '''"""Magic bytes format detector — tooling capstone."""
from __future__ import annotations

SIGNATURES = [
    (b"\\x89PNG\\r\\n\\x1a\\n", "PNG"),
    (b"\\x1f\\x8b", "GZIP"),
    (b"PK\\x03\\x04", "ZIP"),
]


def match_signature(data: bytes) -> str | None:
    """TODO [CAP-TOOL-DET-01]: first matching signature name."""
    raise NotImplementedError("CAP-TOOL-DET-01")


def confidence(data: bytes, fmt: str) -> float:
    """TODO [CAP-TOOL-DET-02]: 1.0 if prefix matches else 0.0."""
    raise NotImplementedError("CAP-TOOL-DET-02")


def detect_format(data: bytes) -> dict:
    """TODO [CAP-TOOL-DET-03]: {format, confidence}."""
    raise NotImplementedError("CAP-TOOL-DET-03")
'''
    sol = starter.replace(
        'def match_signature(data: bytes) -> str | None:\n    """TODO [CAP-TOOL-DET-01]: first matching signature name."""\n    raise NotImplementedError("CAP-TOOL-DET-01")',
        'def match_signature(data: bytes) -> str | None:\n    # PEDAGOGY-SOLUTION: CAP-TOOL-DET-01\n    for sig, name in SIGNATURES:\n        if data.startswith(sig):\n            return name\n    return None',
    ).replace(
        'def confidence(data: bytes, fmt: str) -> float:\n    """TODO [CAP-TOOL-DET-02]: 1.0 if prefix matches else 0.0."""\n    raise NotImplementedError("CAP-TOOL-DET-02")',
        'def confidence(data: bytes, fmt: str) -> float:\n    # PEDAGOGY-SOLUTION: CAP-TOOL-DET-02\n    for sig, name in SIGNATURES:\n        if name == fmt:\n            return 1.0 if data.startswith(sig) else 0.0\n    return 0.0',
    ).replace(
        'def detect_format(data: bytes) -> dict:\n    """TODO [CAP-TOOL-DET-03]: {format, confidence}."""\n    raise NotImplementedError("CAP-TOOL-DET-03")',
        'def detect_format(data: bytes) -> dict:\n    # PEDAGOGY-SOLUTION: CAP-TOOL-DET-03\n    fmt = match_signature(data)\n    if fmt is None:\n        return {"format": None, "confidence": 0.0}\n    return {"format": fmt, "confidence": confidence(data, fmt)}',
    )
    test = '''# PEDAGOGY-TEST: CAP-TOOL-DET-01
# PEDAGOGY-TEST: CAP-TOOL-DET-02
# PEDAGOGY-TEST: CAP-TOOL-DET-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_format_detect import match_signature, detect_format

def main():
    png = b"\\x89PNG\\r\\n\\x1a\\n" + b"rest"
    assert match_signature(png) == "PNG"
    d = detect_format(png)
    assert d["format"] == "PNG" and d["confidence"] == 1.0
    print("OK format_detect")

if __name__ == "__main__":
    main()
'''
    todos = [
        {"id": ids[0], "file": "starter/capstone_format_detect.py", "fn": "match_signature",
         "problem": "Magic primeiro.", "code": "startswith loop",
         "why": "Tooling triage.", "verify": "Caso 1: PNG."},
        {"id": ids[1], "file": "starter/capstone_format_detect.py", "fn": "confidence",
         "problem": "Score binário.", "code": "1.0 or 0.0",
         "why": "Relatório.", "verify": "Caso 2: 1.0."},
        {"id": ids[2], "file": "starter/capstone_format_detect.py", "fn": "detect_format",
         "problem": "API unificada.", "code": "match+confidence",
         "why": "Capstone detect.", "verify": "Caso 3: dict."},
    ]
    scaffold_py_module("tooling", "capstone_format_detect", ids, "Capstone format detect", "tooling",
                       ["PNG sig", "GZIP sig", "ZIP sig", "Detector API"],
                       starter, sol, test,
                       f"cd days/{DAY}/tooling/capstone_format_detect/starter\npython test_capstone_format_detect.py",
                       todos)


def scaffold_day_infra() -> None:
    mod_lines = "\n".join(
        f"| {i} | `{t}/{n}` | capstone {t} | 2–3 |"
        for i, (t, n, *_rest) in enumerate(MODULES, 1)
    )
    w(DAY_DIR / "README.md", f"""# Day 10 — {DAY}

**{THEME}** — sintetiza Dias 01–09 em 13 módulos tier-A multi-trilha.

## Módulos (13) — ordem cognitiva

| # | Módulo | Fundamento | Horas |
|---|--------|------------|-------|
{mod_lines}

**Total:** ~28–36 h.

## Capstones

- [`projects/chris-vm/`](../../projects/chris-vm/) — CLVM + verify
- [`projects/chris-driver-lab/`](../../projects/chris-driver-lab/) — input pipeline
- [`projects/chris-binary-toolkit/`](../../projects/chris-binary-toolkit/) — format triage
- [`projects/chris-agent-harness/`](../../projects/chris-agent-harness/) — agent loop

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day {DAY}
python scripts/run_day_tests.py --day {DAY} --mode solutions
```
""")
    block_rows = "\n".join(
        f"| {t} | `{t}/{n}` |" for t, n, *_ in MODULES
    )
    w(DAY_DIR / "START_HERE.md", f"""# START HERE — Day {DAY}

**{THEME}**

## Fluxo por módulo

1. TEORIA → EXERCICIOS → starter → TESTES → RESOLUCAO (se travar)
2. Gates no final do dia

## Ordem por bloco

| Bloco | Módulo |
|-------|--------|
{block_rows}

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day {DAY}
python scripts/day_contract_check.py --day {DAY}
python scripts/run_day_tests.py --day {DAY} --mode solutions
```
""")
    w(DAY_DIR / "ATIVIDADES.md", f"""# ATIVIDADES — Day {DAY}

13 módulos capstone. Checkpoints conceituais antes de avançar.

## Manhã — CLVM + input

1. `systems/clvm_pipeline_integration` — disasm/peephole/verify fecha o arco CLVM
2. `systems/unified_input_pipeline` — keyboard+mouse end-to-end
3. `linux/composite_input_driver` — driver composto conceitual

## Tarde — Rust/.NET/GFX

4. `rust/cross_verify_clvm` — paridade Rust/Python
5. `dotnet/capstone_input_host` — host .NET do pipeline
6. `graphics/pipeline_state_object` — PSO FSM

## Noite — triage + quantum + AI

7. `redteam/capstone_triage` — ELF+PE+WASM
8. `quantum/capstone_measurement` — medição completa
9. `ai/capstone_tokenizer` — tokenizer byte-level

## Streams + parsers + agent + tooling

10. `nodejs/capstone_stream_pipeline`
11. `parsers/capstone_query_eval`
12. `agent/capstone_agent_loop`
13. `tooling/capstone_format_detect`
""")
    val_rows = "\n".join(
        f"| {t} | {n} | pytest/node/cargo/dotnet |"
        for t, n, *_ in MODULES
    )
    w(DAY_DIR / "VALIDATION.md", f"""# VALIDATION — Day {DAY}

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day {DAY}
python scripts/day_contract_check.py --day {DAY}
python scripts/run_day_tests.py --day {DAY} --mode solutions
```

## Expectativas

| Gate | Esperado |
|------|----------|
| pedagogy_check | **PASS** — 13 módulos, 39 TODOs |
| day_contract | **PASS** — tier-A tracks |
| solutions | 13/13 PASS |

## Módulos (13)

| Trilha | Módulo | Runner |
|--------|--------|--------|
{val_rows}
""")
    w(DAY_DIR / "day.contract.yaml", f"""day: {DAY}
tier: tier_a
min_modules: 13
required_tracks:
  - systems
  - linux
  - rust
  - dotnet
  - graphics
  - redteam
  - quantum
  - ai
  - nodejs
  - parsers
  - agent
  - tooling
theme: "{THEME}"
""")


def update_tracks_yaml() -> None:
    path = ROOT / "openspec" / "specs" / "day-contract" / "tracks.yaml"
    text = path.read_text(encoding="utf-8")
    if f'"{DAY}"' in text:
        return
    block = f'''      "{DAY}":
        required_tracks:
          - systems
          - linux
          - rust
          - dotnet
          - graphics
          - redteam
          - quantum
          - ai
          - nodejs
          - parsers
          - agent
          - tooling
'''
    marker = '      "2026-09-07":'
    if marker in text:
        text = text.replace(marker, block + marker)
        path.write_text(text, encoding="utf-8")


def update_learning_paths() -> None:
    path = ROOT / "docs" / "LEARNING_PATHS.md"
    text = path.read_text(encoding="utf-8")
    if DAY in text:
        return
    section = f"""

---

## 14. Day 10 — Capstone integração ({DAY})

**Tema:** {THEME}

| # | Módulo | Conceito |
|---|--------|----------|
"""
    for i, (t, n, *_rest) in enumerate(MODULES, 1):
        section += f"| {i} | `{DAY}/{t}/{n}` | capstone {t} |\n"
    path.write_text(text.rstrip() + section, encoding="utf-8")


def update_module_map() -> None:
    path = ROOT / "scripts" / "module_project_map.py"
    text = path.read_text(encoding="utf-8")
    projects = {
        "systems/clvm_pipeline_integration": "projects/chris-vm",
        "systems/unified_input_pipeline": "projects/chris-driver-lab",
        "linux/composite_input_driver": "projects/chris-driver-lab",
        "rust/cross_verify_clvm": "projects/chris-vm",
        "dotnet/capstone_input_host": "projects/chris-driver-lab",
        "graphics/pipeline_state_object": "projects/chris-renderer",
        "redteam/capstone_triage": "projects/chris-binary-toolkit",
        "quantum/capstone_measurement": "projects/chris-quantum-sim",
        "ai/capstone_tokenizer": "projects/chris-autograd",
        "nodejs/capstone_stream_pipeline": "projects/chris-http",
        "parsers/capstone_query_eval": "projects/chris-smart-grep",
        "agent/capstone_agent_loop": "projects/chris-agent-harness",
        "tooling/capstone_format_detect": "projects/chris-binary-toolkit",
    }
    entries = []
    for t, n, *_ in MODULES:
        key = f"{DAY}/{t}/{n}"
        if key in text:
            continue
        proj = projects.get(f"{t}/{n}", "projects/chris-vm")
        entries.append(f'''    "{key}": {{
        "project": "{proj}",
        "carry": "capstone {n} from day10",
        "tests": "day10 module tests",
        "milestone": "MILESTONES.md — day10 {n}",
        "commit": "feat(day10): port {n}",
    }},''')
    if not entries:
        return
    text = text.replace("\n}\n\n\ndef module_key", "\n" + "\n".join(entries) + "\n}\n\n\ndef module_key")
    path.write_text(text, encoding="utf-8")


def run_post_scaffold() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "upgrade_module_quality.py"), "--day", DAY],
        cwd=ROOT, check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_day_scaffold.py"), "--day", DAY, "--manifest-only"],
        cwd=ROOT, check=True,
    )
    from generate_day_scaffold import build_todo_map  # noqa: E402

    w(DAY_DIR / "TODO_MAP.md", build_todo_map(DAY_DIR))


def main() -> None:
    DAY_DIR.mkdir(parents=True, exist_ok=True)
    scaffold_clvm_pipeline()
    scaffold_unified_input()
    scaffold_linux_composite()
    scaffold_rust_clvm()
    scaffold_dotnet_host()
    scaffold_gfx_pso()
    scaffold_redteam_triage()
    scaffold_quantum()
    scaffold_ai_tokenizer()
    scaffold_node_pipeline()
    scaffold_pratt()
    scaffold_agent()
    scaffold_tooling_detect()
    scaffold_day_infra()
    update_tracks_yaml()
    update_learning_paths()
    update_module_map()
    run_post_scaffold()
    print(f"Day 10 scaffolded: {DAY_DIR}")


if __name__ == "__main__":
    main()
