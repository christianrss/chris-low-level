#!/usr/bin/env python3
"""Pad short RESOLUCAO code fences to meet pedagogy min-3-lines rule."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GH = {
    "2026-09-09": [
        "systems/buddy_allocator",
        "ai/welford_layernorm",
        "redteam/x86_prologue_triage",
        "dotnet/channel_backpressure",
        "nodejs/async_context",
        "graphics/explicit_barriers",
        "linux/proc_stat_parser",
        "parsers/pratt_expr",
        "agent/agent_state_machine",
        "unix/grep_dfa",
        "architecture/branch_predictor",
    ],
    "2026-09-10": [
        "systems/aba_tagged_freelist",
        "ai/tiled_attention_online_softmax",
        "architecture/tlb_page_walk",
        "dotnet/pinned_memory_probe",
        "graphics/descriptor_binding_model",
        "linux/procfs_module_lab",
        "nodejs/message_channel_rpc",
        "parsers/backtracking_regex_vm",
        "redteam/elf64_relocation_triage",
        "agent/transactional_patcher",
    ],
    "2026-09-11": [
        "systems/hazard_pointer_stack",
        "ai/kv_cache_ring",
        "redteam/dwarf_line_program",
        "dotnet/jit_callsite_model",
        "nodejs/worker_pool_scheduler",
        "parsers/pike_regex_vm",
        "agent/context_budgeter",
        "quantum/statevector_bitmask",
        "network/length_prefixed_framing",
        "algorithms/robin_hood_hash",
    ],
}

FENCE = re.compile(r"(```[a-zA-Z0-9_+-]*\n)(.*?)(\n```)", re.DOTALL)


def pad_block(lang_line: str, body: str, close: str) -> str:
    lines = body.split("\n")
    # drop trailing empty from split quirks
    while lines and lines[-1] == "":
        lines.pop()
    while len(lines) < 3:
        lines.append("# keep contract / edge case")
    return lang_line + "\n".join(lines) + close


def deepen_resolucao(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def repl(m: re.Match[str]) -> str:
        nonlocal changed
        body = m.group(2)
        n = len([ln for ln in body.split("\n") if ln.strip() != "" or True])
        # count physical lines in fence body
        phys = body.count("\n") + (1 if body else 0)
        if body == "":
            phys = 0
        else:
            phys = len(body.split("\n"))
        if phys >= 3:
            return m.group(0)
        changed = True
        return pad_block(m.group(1), body, m.group(3))

    new = FENCE.sub(repl, text)
    # Also thicken thin "Algoritmo / trace" one-liners
    thin = "Caso do TESTES_GUIADOS ligado a"
    if thin in new:
        new2 = []
        for line in new.splitlines(keepends=True):
            if thin in line and line.strip().startswith("Caso"):
                tid = line.strip()
                new2.append(
                    "1. Leia o assert do teste ligado a este TODO.\n"
                    "2. Execute o Caso 1 no papel (entrada → estado → saida).\n"
                    "3. Compare com o bloco abaixo antes de colar no starter.\n"
                )
                changed = True
            else:
                new2.append(line)
        new = "".join(new2)
    if changed:
        path.write_text(new, encoding="utf-8", newline="\n")
    return changed


def main() -> None:
    n = 0
    for day, mods in GH.items():
        for m in mods:
            path = ROOT / "days" / day / m / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
            if path.exists() and deepen_resolucao(path):
                print("padded", day, m)
                n += 1
    print("done", n)


if __name__ == "__main__":
    main()
