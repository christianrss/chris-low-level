#!/usr/bin/env python3
"""Remove generic Verifique stubs injected by repair_resolucao_strict."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERIC_VERIF = re.compile(
    r"\r?\n### 5\. Verifique\r?\n\r?\n"
    r"Rode os testes do módulo com `TODO \[[A-Z0-9-]+\]` implementado\.\r?\n\r?\n"
    r"\*\*Esperado:\*\* caso\(s\) em TESTES_GUIADOS que cobrem `[A-Z0-9-]+` passam\.\r?\n\r?\n",
    re.MULTILINE,
)


def main() -> int:
    count = 0
    for path in ROOT.glob("days/*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"):
        text = path.read_text(encoding="utf-8")
        new = GENERIC_VERIF.sub("\n", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            count += 1
            print("cleaned", path.relative_to(ROOT))
    print(f"cleanup_generic_verifique: {count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
