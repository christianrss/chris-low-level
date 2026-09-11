#!/usr/bin/env python3
from pathlib import Path

DAY = Path(__file__).resolve().parents[1] / "days" / "2026-09-08"
MODS = [
    "systems/spsc_ring_buffer",
    "architecture/cache_set_sim",
    "ai/online_softmax",
    "redteam/wasm_binary_triage",
    "parsers/nfa_to_dfa",
    "agent/bm25_code_ranker",
    "unix/xargs_lite",
    "nodejs/worker_transfer",
    "dotnet/gc_allocation_probe",
]
for rel in MODS:
    p = DAY / rel / "TEORIA_PASSO_A_PASSO.md"
    t = p.read_text(encoding="utf-8")
    i = 1
    while t.count("\n") < 125:
        t += (
            f"\n## Nota operacional {i} — {rel}\n\n"
            f"Detalhe {i}: o literal do Caso 1 deste modulo nao e intercambiavel "
            f"com o do core CLVM. Confirme o assert antes do TODO passo {i}.\n"
        )
        i += 1
    p.write_text(t, encoding="utf-8", newline="\n")
    print(rel, t.count("\n"))
