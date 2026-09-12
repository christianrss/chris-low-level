#!/usr/bin/env python3
"""Generate START_HERE.md, TODO_MAP.md, MANIFEST.json for a day folder."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from depth_manifest import load_yaml

ROOT = Path(__file__).resolve().parents[1]
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
CODE_EXT = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js", ".cs", ".rs", ".asm", ".s", ".yar", ".sh"}


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def collect_todos(starter: Path) -> list[tuple[str, Path]]:
    items: list[tuple[str, Path]] = []
    for p in starter.rglob("*"):
        if p.is_file() and p.suffix.lower() in CODE_EXT:
            for ident in TODO_RE.findall(p.read_text(encoding="utf-8")):
                items.append((ident, p.relative_to(starter)))
    return items


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_todo_map(day_dir: Path) -> str:
    lines = ["# Mapa global de TODOs\n"]
    for module in find_modules(day_dir):
        rel_mod = module.relative_to(day_dir).as_posix()
        starter = module / "starter"
        if not starter.exists():
            continue
        for ident, rp in collect_todos(starter):
            lines.append(f"## `{ident}`\n")
            lines.append(f"- **Módulo:** `{rel_mod}`")
            lines.append(f"- **Starter:** `starter/{rp.as_posix()}`")
            lines.append(f"- **Resolução:** `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`")
            lines.append(f"- **Teste:** `TESTES_GUIADOS.md` + `PEDAGOGY-TEST: {ident}`")
            lines.append(f"- **Solution:** `solutions/{rp.as_posix()}` + `PEDAGOGY-SOLUTION: {ident}`")
            lines.append("")
    return "\n".join(lines)


def build_start_here(day_dir: Path) -> str:
    date = day_dir.name
    modules = find_modules(day_dir)
    contract_path = day_dir / "day.contract.yaml"
    contract = load_yaml(contract_path) if contract_path.exists() else {}
    if contract.get("profile") == "depth_first":
        project = modules[0].relative_to(day_dir).as_posix() if len(modules) == 1 else "<projeto>"
        return f"""# START HERE — Day {date}

**Perfil:** depth-first | **Projeto:** `{project}` | **Carga:** 6–8 h

## Fluxo

1. Leia o brief, a teoria e o `ASSESSMENT.yaml`.
2. Execute o starter e registre a previsão das falhas.
3. Siga M1–M6 em `ATIVIDADES.md` e `EXERCICIOS.md`.
4. Construa o núcleo nos arquivos `student_owned`; o starter contém apenas infraestrutura.
5. Adicione testes de fronteira antes de consultar a resolução.
6. Use a ajuda progressiva da resolução somente após registrar sua hipótese.
7. Execute benchmark, rejeite os mutantes críticos e preencha `RUBRIC.md`.

## Gates

```powershell
python scripts/day_contract_check.py --day {date}
python scripts/pedagogy_check_unified.py --day {date}
python scripts/run_day_tests.py --day {date} --mode starter --expect-fail
python scripts/run_day_tests.py --day {date} --mode solutions
python scripts/run_depth_mutants.py --day {date}
python scripts/cycle_contract_check.py --cycle {contract.get("cycle", "<cycle>")}
```

DOCX é export opcional; Markdown é a fonte primária.
"""
    mod_list = "\n".join(
        f"{i}. `{m.relative_to(day_dir).as_posix()}`" for i, m in enumerate(modules, 1)
    )
    return f"""# START HERE — Day {date}

Laboratório unificado de low-level. O estudo é **modular**: cada pasta
`<trilha>/<modulo>/` contém teoria, exercícios, resolução guiada e código.

## Fluxo por módulo

1. Leia `README.md` e `TEORIA_PASSO_A_PASSO.md` (≥120 linhas, diagramas, O quê/Como/Por quê).
2. Abra `EXERCICIOS.md` — quatro níveis: Fácil → Médio → Difícil → Desafio.
3. Implemente no `starter/` seguindo os `TODO [ID]` (veja `TODO_MAP.md`).
4. Rode testes — procure `PEDAGOGY-TEST: ID` nos arquivos de teste.
5. Consulte `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar; inclui
   mapa starter→TODO, placement por TODO e Relatório de resolução.
6. Compare com `solutions/` após tentativa honesta; registre benchmark em `BENCHMARK_GUIADO.md`.

## Ordem recomendada

{mod_list}

## Gates de qualidade

```bash
python scripts/pedagogy_check_unified.py --day {date}
python scripts/day_contract_check.py --day {date}
python scripts/run_day_tests.py --day {date} --mode solutions
python scripts/run_day_tests.py --day {date} --mode starter --expect-fail
```

Opcional: export DOCX via `python scripts/build_day_docx.py --day {date}`.
"""


def build_manifest(day_dir: Path) -> dict:
    files = []
    for p in sorted(day_dir.rglob("*")):
        if not p.is_file():
            continue
        skip = {
            "build",
            "build_ci",
            "build_bench",
            "node_modules",
            "__pycache__",
            ".git",
            "bin",
            "obj",
            "CMakeFiles",
            "target",
            ".vs",
            ".cache",
            "TestResults",
            "BenchmarkDotNet.Artifacts",
            "dist",
            "out",
        }
        if any(
            part in skip or part.startswith("build-") or part.startswith("build_")
            for part in p.parts
        ):
            continue
        rel = p.relative_to(day_dir).as_posix()
        files.append({"path": rel, "size": p.stat().st_size, "sha256": sha256_file(p)})
    manifest = {"day": day_dir.name, "file_count": len(files), "files": files}
    manifest["modules"] = len(find_modules(day_dir))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", required=True)
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Only regenerate MANIFEST.json (do not touch START_HERE or TODO_MAP)",
    )
    parser.add_argument(
        "--overwrite-docs",
        action="store_true",
        help="Overwrite START_HERE.md and TODO_MAP.md with generated templates",
    )
    args = parser.parse_args()
    day_dir = ROOT / "days" / args.day
    if not day_dir.exists():
        print(f"Not found: {day_dir}")
        return 1

    manifest = build_manifest(day_dir)
    (day_dir / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    if args.manifest_only:
        print(f"MANIFEST only for {args.day} ({manifest['modules']} modules)")
        return 0

    if args.overwrite_docs:
        (day_dir / "START_HERE.md").write_text(build_start_here(day_dir), encoding="utf-8")
        (day_dir / "TODO_MAP.md").write_text(build_todo_map(day_dir), encoding="utf-8")
        print(f"Scaffold written for {args.day} (docs overwritten)")
        return 0

    print(
        f"MANIFEST written for {args.day}. "
        "Use --overwrite-docs to regenerate START_HERE/TODO_MAP, or --manifest-only alone."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
