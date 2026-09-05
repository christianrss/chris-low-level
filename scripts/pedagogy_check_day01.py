from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days" / "2026-09-03"
CODE_EXTENSIONS = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".rs", ".s", ".asm", ".yar"}
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
UNTAGGED_TODO_RE = re.compile(r"(?:^|\s)(?://|#|/\*)\s*TODO\b(?!\s*\[[A-Z0-9-]+\])")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def main() -> int:
    errors: list[str] = []
    modules = sorted(p.parent for p in DAY.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))
    if not modules:
        print("pedagogy check: no Day01 modules found", file=sys.stderr)
        return 2

    total_ids = 0
    for module in modules:
        rel_module = module.relative_to(ROOT)
        required = [
            module / "TEORIA_PASSO_A_PASSO.md",
            module / "PESQUISA_GUIADA.md",
            module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md",
            module / "TESTES_GUIADOS.md",
            module / "starter",
            module / "solutions",
        ]
        for path in required:
            if not path.exists():
                fail(errors, f"{rel_module}: missing {path.name}")

        starter = module / "starter"
        solution = module / "solutions"
        if not starter.exists() or not solution.exists():
            continue

        resolution = read_text(module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md")
        tests_guide = read_text(module / "TESTES_GUIADOS.md")

        ids_by_file: dict[Path, list[str]] = {}
        untagged: list[str] = []
        for path in starter.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in CODE_EXTENSIONS:
                continue
            text = read_text(path)
            ids = TODO_RE.findall(text)
            if ids:
                ids_by_file[path.relative_to(starter)] = ids
            # Ignore human prose in string literals only imperfectly; code TODO comments must be tagged.
            if "TODO" in text:
                cleaned = TODO_RE.sub("", text)
                if UNTAGGED_TODO_RE.search(cleaned):
                    untagged.append(str(path.relative_to(starter)))

        if untagged:
            fail(errors, f"{rel_module}: untagged TODO in {sorted(set(untagged))}")

        module_ids: list[str] = []
        for rel, ids in ids_by_file.items():
            sol_file = solution / rel
            if not sol_file.exists():
                fail(errors, f"{rel_module}: starter/{rel} has TODO but solutions/{rel} is missing")
                continue
            starter_bytes = (starter / rel).read_bytes()
            solution_bytes = sol_file.read_bytes()
            if starter_bytes == solution_bytes:
                fail(errors, f"{rel_module}: starter/{rel} contains TODO but solution is byte-identical")
            sol_text = read_text(sol_file)
            for ident in ids:
                total_ids += 1
                module_ids.append(ident)
                if ident not in resolution:
                    fail(errors, f"{rel_module}: {ident} missing from guided resolution")
                if ident not in tests_guide:
                    fail(errors, f"{rel_module}: {ident} missing from test/validation guide")
                if f"PEDAGOGY-SOLUTION: {ident}" not in sol_text:
                    fail(errors, f"{rel_module}: {ident} missing solution marker in solutions/{rel}")
                if TODO_RE.search(sol_text) and ident in TODO_RE.findall(sol_text):
                    fail(errors, f"{rel_module}: {ident} still marked TODO in solution/{rel}")

        if not module_ids:
            fail(errors, f"{rel_module}: no tagged code TODOs found in starter")

        # A programming starter with a tests directory and CMake must actually register tests.
        starter_cmake = starter / "CMakeLists.txt"
        solution_cmake = solution / "CMakeLists.txt"
        if (starter / "tests").exists() and starter_cmake.exists():
            for label, cmake in (("starter", starter_cmake), ("solutions", solution_cmake)):
                if not cmake.exists():
                    fail(errors, f"{rel_module}: {label}/CMakeLists.txt missing")
                    continue
                cmake_text = read_text(cmake)
                if "enable_testing" not in cmake_text or "add_test" not in cmake_text:
                    fail(errors, f"{rel_module}: {label} has tests but CMake does not register them")

        # Resolution must be operational, not a pointer to the answer.
        low = resolution.lower()
        if "a solução final está em `solutions" in low or "a solucao final esta em `solutions" in low:
            fail(errors, f"{rel_module}: resolution delegates required implementation to solutions instead of teaching it")

    if errors:
        print("PEDAGOGY CHECK FAILED")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"pedagogy check passed: {len(modules)} modules, {total_ids} starter TODO mappings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
