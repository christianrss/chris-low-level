from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXT = {".c", ".cc", ".cpp", ".h", ".hpp", ".py", ".rs", ".glsl", ".vert", ".frag"}
TEXT_EXT = SOURCE_EXT | {".md", ".txt", ".yml", ".yaml", ".cmake"}
issues: list[str] = []
checked = 0

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in TEXT_EXT:
        continue
    if any(
        part in {"build", "target", ".git", ".local-build", ".local-build-bench"}
        or part.startswith("build-")
        for part in path.parts
    ):
        continue

    text = path.read_text(encoding="utf-8", errors="replace")
    checked += 1
    lines = text.splitlines()

    if len(lines) <= 1 and len(text) > 200:
        issues.append(f"{path.relative_to(ROOT)}: suspicious single-line file")

    if path.suffix.lower() in SOURCE_EXT:
        for line_number, line in enumerate(lines, 1):
            if len(line) > 140:
                issues.append(
                    f"{path.relative_to(ROOT)}:{line_number}: "
                    f"source line length {len(line)}"
                )

        if "\t" in text:
            issues.append(f"{path.relative_to(ROOT)}: tab found in source")

print(f"quality files checked: {checked}")
if issues:
    print("\n".join(issues[:100]))
    raise SystemExit(1)

print("quality check passed")
