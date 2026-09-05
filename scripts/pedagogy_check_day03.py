from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days/2026-09-05"
modules = [p.parent for p in DAY.rglob("TEORIA_PASSO_A_PASSO.md")]
errors = []
mappings = 0
required = [
    "README.md",
    "TEORIA_PASSO_A_PASSO.md",
    "PESQUISA_GUIADA.md",
    "RESOLUCAO_GUIADA_PASSO_A_PASSO.md",
    "TESTES_GUIADOS.md",
    "BENCHMARK_GUIADO.md",
]
for module in modules:
    for name in required:
        if not (module / name).exists():
            errors.append(f"{module}: missing {name}")
    starter_text = "\n".join(
        path.read_text(errors="ignore")
        for path in (module / "starter").rglob("*")
        if path.is_file()
    )
    solution_text = "\n".join(
        path.read_text(errors="ignore")
        for path in (module / "solutions").rglob("*")
        if path.is_file()
    )
    resolution = (
        module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    ).read_text(errors="ignore")
    tests = (module / "TESTES_GUIADOS.md").read_text(errors="ignore")
    todo_ids = sorted(set(re.findall(r"TODO \[([A-Z0-9-]+)\]", starter_text)))
    for todo_id in todo_ids:
        mappings += 1
        if todo_id not in resolution:
            errors.append(f"{module}: {todo_id} missing resolution")
        if todo_id not in tests:
            errors.append(f"{module}: {todo_id} missing tests guide")
        review_only = "REVIEW" in todo_id or "SOURCE" in todo_id
        if todo_id not in solution_text and not review_only:
            errors.append(f"{module}: {todo_id} missing solution trace")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(
    f"day03 pedagogy check passed: {len(modules)} modules, "
    f"{mappings} TODO mappings"
)
