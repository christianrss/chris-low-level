"""Tag bare TODOs and synthesize IDs for v2 modules lacking tags."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "days/2026-09-05-v2/modules"
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
CODE_EXT = {".c", ".cpp", ".h", ".hpp", ".py", ".js", ".cs", ".ts", ".cc", ".cxx"}


def synth_id(mod_name: str) -> str:
    slug = mod_name.split("_", 1)[-1][:16].upper().replace("-", "_")
    return f"V2-{slug}-01"


def main() -> None:
    for mod in sorted(ROOT.iterdir()):
        if not mod.is_dir():
            continue
        starter = mod / "starter"
        if not starter.exists():
            continue
        files = [
            p
            for p in starter.rglob("*")
            if p.is_file() and p.suffix.lower() in CODE_EXT
        ]
        tagged: list[str] = []
        for p in files:
            tagged.extend(TODO_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))

        ident = synth_id(mod.name)

        # Replace first bare TODO in each file that still has bare TODO
        for p in files:
            text = p.read_text(encoding="utf-8", errors="ignore")
            if not re.search(r"\bTODO\b(?!\s*\[)", text):
                continue
            text2 = re.sub(r"\bTODO\b(?!\s*\[)", f"TODO [{ident}]", text, count=1)
            if text2 != text:
                p.write_text(text2, encoding="utf-8")
                print("tagged bare", mod.name, p.name, ident)
                tagged.append(ident)

        if tagged:
            continue

        prefer = [
            "Program.cs",
            "vm.js",
            "line_transform.js",
            "resource_states.cpp",
            "states.cpp",
            "backpressure_demo.js",
        ]
        target = None
        for name in prefer:
            for p in files:
                if p.name == name:
                    target = p
                    break
            if target:
                break
        if not target and files:
            target = files[0]
        if not target:
            print("skip empty", mod.name)
            continue

        pref = "//" if target.suffix.lower() in {".c", ".cpp", ".h", ".hpp", ".js", ".cs"} else "#"
        text = target.read_text(encoding="utf-8", errors="ignore")
        target.write_text(f"{pref} TODO [{ident}]: complete lab stubs\n" + text, encoding="utf-8")
        print("created", mod.name, target.name, ident)
        sol = mod / "solutions" / target.relative_to(starter)
        if sol.exists():
            st = sol.read_text(encoding="utf-8", errors="ignore")
            mark = f"PEDAGOGY-SOLUTION: {ident}"
            if mark not in st:
                sol.write_text(f"{pref} {mark}\n" + st, encoding="utf-8")


if __name__ == "__main__":
    main()
