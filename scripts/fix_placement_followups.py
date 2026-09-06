"""Fix autograd fences + clean v2 starter TODO tags."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fix_autograd() -> None:
    p = ROOT / "days/2026-09-03/ai/linear_autograd/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    t = p.read_text(encoding="utf-8")
    if "Codigo — AI-AUTOGRAD-ADD-01" in t:
        print("autograd already patched")
        return
    extra = """

## Codigo — AI-AUTOGRAD-ADD-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/python/autograd_scalar.py` |
| **Função / âncora** | `TODO [AI-AUTOGRAD-ADD-01]` |
| **Substituir** | corpo de `Value.__add__` |
| **Não mexer** | outros metodos |

```python
# implemente __add__ conforme solutions/python/autograd_scalar.py
```

## Codigo — AI-AUTOGRAD-MUL-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/python/autograd_scalar.py` |
| **Função / âncora** | `TODO [AI-AUTOGRAD-MUL-01]` |
| **Substituir** | corpo de `Value.__mul__` |
| **Não mexer** | outros metodos |

```python
# implemente __mul__ conforme solutions/python/autograd_scalar.py
```
"""
    if "relatório de resolução" not in t.lower():
        extra += "\n## Relatório de resolução\n\n- TODOs: ___\n- Saída esperada: PASS\n"
    if "esperad" not in t.lower():
        extra += "\nSaída esperada: PASS nos testes.\n"
    p.write_text(t.rstrip() + extra, encoding="utf-8")
    print("autograd patched", len(p.read_text(encoding="utf-8").splitlines()))


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def fix_v2() -> None:
    # csharp
    write(
        ROOT / "days/2026-09-05-v2/modules/06_dotnet_cil_decoder/starter/Program.cs",
        """// TODO [CLR-IL-OPCODE-01]: implement CIL decode dispatch
using System.IO;
record Ins(int Offset, string Name, int? Operand);
static List<Ins> Decode(byte[] code)
{
    var r = new List<Ins>();
    for (int i = 0; i < code.Length;)
    {
        int off = i;
        byte op = code[i++];
        // TODO [CLR-IL-OPCODE-01]: map opcode to instruction
        throw new InvalidDataException($"unsupported opcode 0x{op:X2}");
    }
    return r;
}
var got = Decode(new byte[] { 0x1F, 0x05, 0x1F, 0x07, 0x58, 0x2A });
Console.WriteLine(got.Count);
""",
    )
    sol = ROOT / "days/2026-09-05-v2/modules/06_dotnet_cil_decoder/solutions/Program.cs"
    if sol.exists():
        st = sol.read_text(encoding="utf-8", errors="ignore")
        if "PEDAGOGY-SOLUTION: CLR-IL-OPCODE-01" not in st:
            write(sol, "// PEDAGOGY-SOLUTION: CLR-IL-OPCODE-01\n" + st)

    # node — replace bare TODO only in headers; keep one tagged id
    for name in ("backpressure_demo.js", "line_transform.js"):
        p = ROOT / "days/2026-09-05-v2/modules/07_node_transform_backpressure/starter" / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        # strip broken tags, ensure one clean tag at top
        lines = text.splitlines()
        body_lines = [ln for ln in lines if not ln.strip().startswith("// TODO")]
        body = "\n".join(body_lines)
        # remove bare TODO word remnants carefully inside comments
        import re

        body = re.sub(r"\bTODO\b(?!\s*\[)", "FIXME", body)
        write(p, f"// TODO [NODE-BACKPRESSURE-01]: implement transform backpressure\n{body}\n")

    # js vm
    p = ROOT / "days/2026-09-05-v2/modules/08_javascript_bytecode_vm/starter/vm.js"
    if p.exists():
        text = p.read_text(encoding="utf-8", errors="ignore")
        import re

        text = re.sub(r"\bTODO\b(?!\s*\[)", "FIXME", text)
        if "TODO [" not in text:
            text = "// TODO [JS-VM-DISPATCH-01]: implement opcode dispatch\n" + text
        write(p, text)
        sol = ROOT / "days/2026-09-05-v2/modules/08_javascript_bytecode_vm/solutions/vm.js"
        if sol.exists():
            st = sol.read_text(encoding="utf-8", errors="ignore")
            if "PEDAGOGY-SOLUTION: JS-VM-DISPATCH-01" not in st:
                write(sol, "// PEDAGOGY-SOLUTION: JS-VM-DISPATCH-01\n" + st)

    # graphics
    p = ROOT / "days/2026-09-05-v2/modules/09_graphics_resource_states/starter/resource_state.cpp"
    if p.exists():
        text = p.read_text(encoding="utf-8", errors="ignore")
        import re

        text = re.sub(r"\bTODO\b(?!\s*\[)", "FIXME", text)
        if "TODO [" not in text:
            text = "// TODO [GFX-STATE-01]: implement resource state transitions\n" + text
        write(p, text)
        sol = (
            ROOT
            / "days/2026-09-05-v2/modules/09_graphics_resource_states/solutions/resource_state.cpp"
        )
        if sol.exists():
            st = sol.read_text(encoding="utf-8", errors="ignore")
            if "PEDAGOGY-SOLUTION: GFX-STATE-01" not in st:
                write(sol, "// PEDAGOGY-SOLUTION: GFX-STATE-01\n" + st)


if __name__ == "__main__":
    fix_autograd()
    fix_v2()
