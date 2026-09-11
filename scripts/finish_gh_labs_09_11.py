#!/usr/bin/env python3
"""Scaffold day 10–11 GitHub labs + refresh infra with correct newlines."""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def W(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def refresh_infra(day: str, core_note: str) -> None:
    day_dir = ROOT / "days" / day
    mods = sorted(
        p.relative_to(day_dir).as_posix()
        for p in day_dir.glob("*/*")
        if p.is_dir() and (p / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").exists()
    )
    n = len(mods)
    ids: list[str] = []
    seen: set[str] = set()
    for m in mods:
        starter = day_dir / m / "starter"
        if not starter.exists():
            continue
        for p in starter.rglob("*"):
            if not p.is_file():
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for tid in re.findall(r"TODO\s*\[([A-Z0-9-]+)\]", t):
                if tid not in seen:
                    seen.add(tid)
                    ids.append(tid)
    W(day_dir / "TODO_MAP.md", f"# TODO map — {day}\n\n" + "\n".join(f"- `{i}`" for i in ids) + "\n")
    W(
        day_dir / "VALIDATION.md",
        f"""# Validacao — {day}

```powershell
python scripts/pedagogy_check_unified.py --day {day}
python scripts/day_contract_check.py --day {day}
python scripts/run_day_tests.py --day {day} --mode solutions
```

## Modulos ({n})

"""
        + "\n".join(f"- `{m}`" for m in mods)
        + "\n",
    )
    W(
        day_dir / "README.md",
        f"""# Day {day}

**{n} modulos** — core local + labs sugeridos do GitHub incorporados.

{core_note}

| # | Modulo |
|---|--------|
"""
        + "\n".join(f"| {i} | `{m}` |" for i, m in enumerate(mods, 1))
        + f"""

**Total:** ~{n * 2}–{n * 3} h (fatie se preciso).
""",
    )
    cores = {
        "2026-09-09": {
            "systems/clvm_trace_profiler",
            "systems/arena_telemetry",
            "ai/attention_mask",
            "rust/stack_sample_trace",
            "dotnet/activity_source_span",
            "nodejs/async_hooks_trace",
            "linux/perf_event_open_lab",
            "graphics/gpu_timer_query",
            "parsers/logfmt_lexer",
            "quantum/decoherence_noise",
            "redteam/yara_match_scan",
            "agent/verify_replay_log",
            "tooling/pdb_symbol_index",
        },
        "2026-09-10": {
            "systems/clvm_pipeline_integration",
            "systems/unified_input_pipeline",
            "linux/composite_input_driver",
            "rust/cross_verify_clvm",
            "dotnet/capstone_input_host",
            "graphics/pipeline_state_object",
            "redteam/capstone_triage",
            "quantum/capstone_measurement",
            "ai/capstone_tokenizer",
            "nodejs/capstone_stream_pipeline",
            "parsers/capstone_query_eval",
            "agent/capstone_agent_loop",
            "tooling/capstone_format_detect",
        },
        "2026-09-11": {
            "systems/clvm_reloc_apply",
            "systems/bump_poison_arena",
            "linux/uevent_kv_parse",
            "rust/clvm_reloc_verify",
            "dotnet/pe_import_span",
            "graphics/alpha_blend_scanline",
            "redteam/import_name_triage",
            "quantum/phase_kickback",
            "ai/rms_norm",
            "nodejs/shared_atomics_ring",
            "parsers/ini_rd_lexer",
            "agent/tool_barrier_join",
            "tooling/coff_sym_name",
        },
    }
    core = cores.get(day, set())
    gh_mods = [m for m in mods if m not in core]
    gh_lines = "\n".join(
        f"- [ ] `{m}` — implementar TODOs; paper-trace do Caso 1" for m in gh_mods
    )
    W(
        day_dir / "ATIVIDADES.md",
        f"""# Atividades — {day}

## Trilha core (local)

{core_note}

Ver START_HERE / README para ordem sugerida dos módulos core.

## Trilha GitHub (labs incorporados)

{gh_lines}

**Checkpoint trilha GitHub:**

- [ ] Listei os {len(gh_mods)} labs novos no caderno
- [ ] Rodei solutions desses labs

```powershell
python scripts/run_day_tests.py --day {day} --mode solutions
```
""",
    )
    print(day, "infra", n, "modules", "gh", len(gh_mods))


def wire_maps() -> None:
    lp = ROOT / "docs" / "LEARNING_PATHS.md"
    lt = lp.read_text(encoding="utf-8")
    mp = ROOT / "scripts" / "module_project_map.py"
    mt = mp.read_text(encoding="utf-8")
    new_entries: list[str] = []
    for day in ("2026-09-09", "2026-09-10", "2026-09-11"):
        day_dir = ROOT / "days" / day
        for p in sorted(day_dir.glob("*/*")):
            if not (p / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").exists():
                continue
            key = f"{day}/{p.parent.name}/{p.name}"
            if key not in lt:
                new_entries.append(key)
            if f'"{key}"' not in mt:
                proj = "projects/chris-binary-toolkit"
                if "/agent/" in key:
                    proj = "projects/chris-agent-core"
                elif "regex" in key or "/parsers/" in key:
                    proj = "projects/chris-regex"
                elif "/dotnet/" in key:
                    proj = "projects/chris-dotnet-bench"
                elif "/graphics/" in key:
                    proj = "projects/chris-renderer"
                elif "/linux/" in key:
                    proj = "projects/chris-linux-utils"
                elif "/quantum/" in key:
                    proj = "projects/chris-qsim"
                elif "/ai/" in key:
                    proj = "projects/chris-tensor"
                elif "/nodejs/" in key:
                    proj = "projects/chris-node-streaming"
                elif "/unix/" in key:
                    proj = "projects/chris-grep"
                block = f'''
    "{key}": {{
        "project": "{proj}",
        "carry": "{p.name} from github track",
        "tests": "day module tests",
        "milestone": "MILESTONES.md — {p.name}",
        "commit": "feat({day}): port {p.name}",
    }},'''
                if "\ndef module_key" in mt:
                    pre, post = mt.split("\ndef module_key", 1)
                    pre = pre.rstrip()
                    if pre.endswith("}"):
                        pre = pre[:-1].rstrip()
                        if not pre.endswith(","):
                            pre += ","
                        mt = pre + block + "\n}\n\ndef module_key" + post
    if new_entries and "Labs GitHub incorporados (09–11)" not in lt:
        rows = "\n".join(
            f"| {i} | `{k}` | github track |" for i, k in enumerate(new_entries, 1)
        )
        lt = lt.rstrip() + "\n\n### Labs GitHub incorporados (09–11)\n\n" + rows + "\n"
        lp.write_text(lt, encoding="utf-8", newline="\n")
    mp.write_text(mt, encoding="utf-8", newline="\n")

    ped = ROOT / "scripts" / "pedagogy_check_unified.py"
    pt = ped.read_text(encoding="utf-8")
    for name in ("explicit_barriers", "descriptor_binding_model"):
        if f'"{name}"' not in pt:
            pt = pt.replace(
                '"alpha_blend_scanline",',
                f'"alpha_blend_scanline",\n    "{name}",',
            )
    ped.write_text(pt, encoding="utf-8", newline="\n")


def main() -> None:
    s9 = _load("s9", ROOT / "scripts" / "scaffold_github_labs_09_11.py")
    b = _load("b", ROOT / "scripts" / "scaffold_github_labs_09_11_b.py")
    if not (ROOT / "days/2026-09-09/systems/buddy_allocator").exists():
        s9.day09()
    if not (ROOT / "days/2026-09-10/systems/aba_tagged_freelist").exists():
        b.day10()
    if not (ROOT / "days/2026-09-11/systems/hazard_pointer_stack").exists():
        b.day11()
    for d, note in (
        ("2026-09-09", "Core: observabilidade. GitHub: buddy/Welford/prologue/pratt/…"),
        ("2026-09-10", "Core: capstone. GitHub: ABA/TLB/regex/patcher/…"),
        ("2026-09-11", "Core: reloc/ABI. GitHub: hazard/KV/DWARF/Pike/…"),
    ):
        refresh_infra(d, note)
    wire_maps()
    for day in ("2026-09-09", "2026-09-10", "2026-09-11"):
        subprocess.check_call(
            [
                sys.executable,
                str(ROOT / "scripts" / "generate_day_scaffold.py"),
                "--day",
                day,
                "--manifest-only",
            ],
            cwd=ROOT,
        )
    print("all done")


if __name__ == "__main__":
    main()
