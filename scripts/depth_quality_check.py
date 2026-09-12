"""Semantic quality checks for depth-first learning days."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from day_contract_check import find_modules, load_day_contract
from depth_manifest import load_yaml

CODE_EXT = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js",
    ".mjs", ".cs", ".rs", ".asm", ".s", ".glsl", ".hlsl",
}
SKIP_PARTS = {"build", "build_ci", "node_modules", "target", "bin", "obj"}


def substantive_lines(path: Path) -> int:
    if path.suffix.lower() not in CODE_EXT:
        return 0
    count = 0
    in_block = False
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        if in_block:
            if "*/" in line:
                in_block = False
            continue
        if line.startswith("/*"):
            in_block = "*/" not in line
            continue
        if line.startswith(("//", "#", ";", "*")):
            continue
        count += 1
    return count


def expand_files(module: Path, patterns: list[Any]) -> list[Path]:
    found: set[Path] = set()
    for raw in patterns:
        pattern = str(raw)
        for path in module.glob(pattern):
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.is_file():
                found.add(path)
            elif path.is_dir():
                found.update(
                    item for item in path.rglob("*")
                    if item.is_file() and not any(part in SKIP_PARTS for part in item.parts)
                )
    return sorted(found)


def resolve_test(module: Path, reference: str) -> Path | None:
    rel = reference.split("::", 1)[0]
    for base in (module, module / "starter", module / "solutions"):
        candidate = base / rel
        if candidate.is_file():
            return candidate
    return None


def ids(rows: list[Any]) -> set[str]:
    return {
        str(row.get("id"))
        for row in rows
        if isinstance(row, dict) and row.get("id")
    }


def check_assessment(day_dir: Path) -> list[str]:
    errors: list[str] = []
    contract = load_day_contract(day_dir)
    if not contract or contract.get("profile") != "depth_first":
        return errors

    modules = find_modules(day_dir)
    if len(modules) != 1:
        return [f"{day_dir.name}: depth assessment requires exactly one project"]
    module = modules[0]
    rel_project = module.relative_to(day_dir).as_posix()
    path = day_dir / "ASSESSMENT.yaml"
    if not path.exists():
        return [f"{day_dir.name}: missing ASSESSMENT.yaml"]
    try:
        data = load_yaml(path)
    except (OSError, ValueError) as exc:
        return [str(exc)]

    if data.get("profile") != "depth_first":
        errors.append(f"{day_dir.name}: ASSESSMENT profile must be depth_first")
    if data.get("project") != rel_project:
        errors.append(
            f"{day_dir.name}: ASSESSMENT project {data.get('project')!r} "
            f"!= {rel_project!r}"
        )

    student_patterns = data.get("student_owned") or []
    solution_patterns = data.get("solution_owned") or []
    if not student_patterns or not solution_patterns:
        errors.append(f"{day_dir.name}: ASSESSMENT requires student_owned and solution_owned")
    starter_files = expand_files(module, student_patterns)
    solution_files = expand_files(module, solution_patterns)
    if not starter_files:
        errors.append(f"{day_dir.name}: student_owned patterns match no starter files")
    if not solution_files:
        errors.append(f"{day_dir.name}: solution_owned patterns match no solution files")

    starter_sloc = sum(substantive_lines(item) for item in starter_files)
    solution_sloc = sum(substantive_lines(item) for item in solution_files)
    expected = data.get("expected_student_sloc") or {}
    expected_min = int(expected.get("min", 250)) if isinstance(expected, dict) else int(expected)
    if expected_min < 250:
        errors.append(f"{day_dir.name}: expected_student_sloc.min must be at least 250")
    authored_delta = max(0, solution_sloc - starter_sloc)
    if authored_delta < expected_min:
        errors.append(
            f"{day_dir.name}: authored production delta {authored_delta} SLOC "
            f"is below {expected_min}"
        )
    max_percent = int(data.get("starter_logic_max_percent", 15))
    if max_percent > 15:
        errors.append(f"{day_dir.name}: starter_logic_max_percent cannot exceed 15")
    starter_percent = (starter_sloc * 100 / solution_sloc) if solution_sloc else 100.0
    if starter_percent > max_percent:
        errors.append(
            f"{day_dir.name}: starter contains {starter_percent:.1f}% of solution logic "
            f"(max {max_percent}%)"
        )

    concepts = data.get("concepts") or []
    milestones = data.get("milestones") or []
    behaviors = data.get("behaviors") or []
    failures = data.get("failure_modes") or []
    mutants = data.get("critical_mutants") or []
    if not 6 <= len(milestones) <= 10:
        errors.append(f"{day_dir.name}: ASSESSMENT requires 6-10 milestones")
    if len(behaviors) < 10:
        errors.append(f"{day_dir.name}: ASSESSMENT requires at least 10 behaviors")
    if len(failures) < 4:
        errors.append(f"{day_dir.name}: ASSESSMENT requires at least 4 failure modes")
    if len(mutants) < 2:
        errors.append(f"{day_dir.name}: ASSESSMENT requires at least 2 critical mutants")
    for mutant in mutants:
        if not isinstance(mutant, dict) or not mutant.get("command"):
            errors.append(f"{day_dir.name}: every critical mutant needs a command")

    milestone_ids = ids(milestones)
    behavior_ids = ids(behaviors) | ids(failures)
    if not any(
        isinstance(row, dict) and row.get("kind") == "end_to_end"
        for row in behaviors
    ):
        errors.append(f"{day_dir.name}: ASSESSMENT needs an end_to_end behavior")

    for concept in concepts:
        if not isinstance(concept, dict):
            errors.append(f"{day_dir.name}: each concept must be a mapping")
            continue
        concept_id = str(concept.get("id") or "<missing>")
        if not concept.get("invariant") or not concept.get("implementation_anchor"):
            errors.append(f"{day_dir.name}: {concept_id} missing invariant/implementation_anchor")
        if concept.get("milestone") not in milestone_ids:
            errors.append(f"{day_dir.name}: {concept_id} references unknown milestone")
        linked = {str(item) for item in concept.get("behaviors") or []}
        if not linked or not linked <= behavior_ids:
            errors.append(f"{day_dir.name}: {concept_id} has invalid behavior links")
        traces = concept.get("traces") or {}
        if not isinstance(traces, dict) or not traces.get("happy") or not traces.get("failure"):
            errors.append(f"{day_dir.name}: {concept_id} needs happy and failure traces")

    for row in [*behaviors, *failures]:
        if not isinstance(row, dict) or not row.get("test"):
            errors.append(f"{day_dir.name}: every behavior/failure needs a test reference")
            continue
        reference = str(row["test"])
        test_path = resolve_test(module, reference)
        if test_path is None:
            errors.append(f"{day_dir.name}: test reference not found: {reference}")
        elif "::" in reference:
            selector = reference.split("::", 1)[1]
            if selector not in test_path.read_text(encoding="utf-8", errors="replace"):
                errors.append(f"{day_dir.name}: test selector not found: {reference}")

    expected_failures = {str(item) for item in data.get("starter_expected_failures") or []}
    if rel_project not in expected_failures:
        errors.append(
            f"{day_dir.name}: starter_expected_failures must include {rel_project}"
        )

    benchmark = data.get("benchmark") or {}
    for key in ("command", "results", "required_metrics"):
        if not isinstance(benchmark, dict) or not benchmark.get(key):
            errors.append(f"{day_dir.name}: benchmark missing {key}")

    rubric = data.get("rubric") or {}
    categories = rubric.get("categories") if isinstance(rubric, dict) else {}
    if not isinstance(categories, dict) or sum(
        int(value) for value in categories.values() if isinstance(value, int)
    ) != 100:
        errors.append(f"{day_dir.name}: rubric categories must total 100")
    if rubric.get("passing_score") != 75 or rubric.get("excellence_score") != 90:
        errors.append(f"{day_dir.name}: rubric thresholds must be 75/90")

    exercises = (module / "EXERCICIOS.md").read_text(encoding="utf-8", errors="replace")
    missing_milestones = sorted(milestone_ids - set(re.findall(r"\bM\d+\b", exercises)))
    if missing_milestones:
        errors.append(
            f"{day_dir.name}: EXERCICIOS missing milestones: {', '.join(missing_milestones)}"
        )
    theory = (module / "TEORIA_PASSO_A_PASSO.md").read_text(
        encoding="utf-8", errors="replace"
    )
    missing_concepts = sorted(ids(concepts) - set(re.findall(r"CONCEPT-[A-Z0-9-]+", theory)))
    if missing_concepts:
        errors.append(
            f"{day_dir.name}: TEORIA missing concepts: {', '.join(missing_concepts)}"
        )
    return errors
