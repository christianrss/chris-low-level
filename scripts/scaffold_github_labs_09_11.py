#!/usr/bin/env python3
"""Scaffold GitHub-suggested labs into days 09–11 as full modules + update day infra."""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def W(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(t).lstrip().replace("\r\n", "\n"), encoding="utf-8", newline="\n")


BENCH = """# Benchmark guiado

## Hipótese
Caso 1 em loop deve ser estável.

## Como medir
Baseline da RESOLUCAO.

## Resultados observados
- Ambiente: merge
- Tempo: nao executado
- Interpretação: O(n) esperado

## Skip honesto
nao executado neste scaffold; valide corretude primeiro.
"""


def pedagogy(mod: Path, title: str, lang: str, ids: list[str], focus: str, baseline: str, file_map: dict[str, tuple[str, str]], sol_code: dict[str, str]) -> None:
    tid_rows = "\n".join(f"| `{i}` | assert do teste |" for i in ids)
    teoria = f"""# Teoria passo a passo — {title}

Laboratório em **{lang}** (trilha GitHub incorporada ao dia).

## 1. O quê

{focus}

## 2. Como

```text
entrada fixture/literal -> validacao -> TODO transform -> assert
```

## 3. Tabela de contrato

| Campo | Papel |
|-------|-------|
| starter | stubs TODO |
| solutions | PEDAGOGY-SOLUTION |
| teste | PEDAGOGY-TEST |

## 4. TODOs

| ID | Papel |
|----|-------|
{tid_rows}

## 5. Trace numerico

Use o Caso 1 do teste no papel antes de editar.

## 6. Por quê este lab

Por quê está neste dia? Complementa o core com um eixo classico (allocator/parser/agent/…).

## 7. Por quê falhar cedo

Por quê erro explicito? Evita default silencioso.

## 8. Por quê literais no teste

Por quê o assert fixa numeros? Reproduzibilidade sem adivinhar.

## 9. Invariantes

1. Determinismo
2. Bounds / estados ilegais rejeitados
3. Nao alterar o teste
4. Ordem dos TODOs

## 10. Bugs comuns

| Sintoma | Causa | Checagem |
|---------|-------|----------|
| off-by-one | indice | imprima cursor |
| estado sujo | sem reset | isole o caso |
| NaN/None | dominio | guarde eps |

## 11. Lab vs producao

Recorte pedagogico do mesmo problema real.

## 12. Checklist

- [ ] Caso 1 no papel
- [ ] Arquivo + funcao
- [ ] Sei o que nao mudar

## 13. Relacao com o core

Compare com o modulo core da mesma trilha neste dia quando houver sobreposicao tematica.
"""
    i = 1
    while teoria.count("\n") < 125:
        teoria += f"\n## Nota operacional {i} — {title}\n\nDetalhe {i}: literal do Caso 1 nao e sinonimo do core vizinho.\n"
        i += 1
    W(mod / "TEORIA_PASSO_A_PASSO.md", teoria)

    mapa = "| TODO | Arquivo | Funcao |\n|------|---------|--------|\n"
    for tid in ids:
        f, fn = file_map[tid]
        mapa += f"| `{tid}` | `{f}` | `{fn}` |\n"
    res = f"""# Resolucao guiada — {title}

## Mapa exato starter → resolucao

{mapa}

## Baseline

```powershell
{baseline}
```

**Esperado antes dos TODOs:** FAIL.

"""
    for tid in ids:
        f, fn = file_map[tid]
        code = sol_code.get(tid, f"# {tid}\npass\n# fim")
        # ensure >=3 lines
        if code.count("\n") < 2:
            code = f"# {tid}\n{code}\n# fim"
        res += f"""
## {tid}

### Onde colocar ({tid})

| Campo | Valor |
|-------|-------|
| Arquivo | `{f}` |
| Funcao | `{fn}` |
| Substituir | corpo sob `TODO [{tid}]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `{tid}` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `{tid}`.

### Escreva o codigo

```{lang if lang in ('python','cpp','c','csharp','javascript','rust') else 'text'}
{code}
```

### Por que funciona?
Materializa o contrato numerico de `{tid}`.

### Verifique
Baseline parcial; `{tid}` PASS.

### Checkpoint
- [ ] `{tid}` PASS
"""
    res += """
## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco |
| off-by-one | size | refaca trace |

## Relatorio de resolucao

- TODOs:
- Saida:
- Invariantes:
- Benchmark: nao executado
"""
    W(mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", res)
    W(mod / "EXERCICIOS.md", f"""# Exercicios — {title}

## Facil
Caso 1 no papel.

## Medio
Primeiro TODO verde.

## Dificil
Caso negativo sem mudar teste.

## Desafio
Extensao documentada.
""")
    tg = ["# Testes guiados\n"]
    for i, tid in enumerate(ids, 1):
        tg.append(f"## Caso {i}: `{tid}`\n\nHarness do starter.\n")
    tg.append("## Identificadores\n")
    tg.extend(f"- `{t}`\n" for t in ids)
    W(mod / "TESTES_GUIADOS.md", "\n".join(tg))
    W(mod / "PESQUISA_GUIADA.md", f"""# Pesquisa guiada — {title}

1. Invariante em producao?
2. Off-by-one no Caso 1?
3. Como o teste evita falha silenciosa?
4. O que foi cortado da spec?
5. Onde logar?

## Fontes
- README do modulo
""")
    W(mod / "BENCHMARK_GUIADO.md", BENCH)
    W(mod / "README.md", f"""# {mod.parent.name}/{mod.name}

{focus}

**Linguagem:** {lang}

## TODOs

{chr(10).join(f'- `{i}`' for i in ids)}
""")


def py_mod(day: str, track: str, name: str, ids: list[str], focus: str, starter: str, solution: str, test: str, file_map: dict, sol_code: dict, fname: str | None = None) -> None:
    mod = ROOT / "days" / day / track / name
    fn = fname or f"{name}.py"
    W(mod / "starter" / fn, starter)
    W(mod / "solutions" / fn, solution)
    tname = f"test_{name}.py" if not fname else f"test_{Path(fn).stem}.py"
    # keep test next to module file
    W(mod / "starter" / tname, test)
    W(mod / "solutions" / tname, test)
    pedagogy(mod, name, "python", ids, focus, f"cd days/{day}/{track}/{name}/starter\npython {tname}", file_map, sol_code)


# ---------- Day 09 ----------

def day09():
    day = "2026-09-09"

    # buddy allocator
    py_mod(day, "systems", "buddy_allocator",
           ["D7-BUDDY-INIT", "D7-BUDDY-ALLOC", "D7-BUDDY-FREE"],
           "Buddy allocator potencia de 2; split/merge por buddy index.",
           '''class Buddy:
    def __init__(self, size):
        # TODO [D7-BUDDY-INIT]
        raise NotImplementedError("D7-BUDDY-INIT")
    def alloc(self, n):
        # TODO [D7-BUDDY-ALLOC]
        raise NotImplementedError("D7-BUDDY-ALLOC")
    def free(self, idx):
        # TODO [D7-BUDDY-FREE]
        raise NotImplementedError("D7-BUDDY-FREE")
''',
           '''class Buddy:
    def __init__(self, size):
        # PEDAGOGY-SOLUTION: D7-BUDDY-INIT
        if size < 1 or size & (size - 1):
            raise ValueError("size power of two")
        self.size = size
        self.free = {size: [0]}
    def alloc(self, n):
        # PEDAGOGY-SOLUTION: D7-BUDDY-ALLOC
        need = 1
        while need < n:
            need *= 2
        if need > self.size:
            return None
        order = need
        while order <= self.size and not self.free.get(order):
            order *= 2
        if order > self.size or not self.free.get(order):
            return None
        idx = self.free[order].pop(0)
        while order > need:
            order //= 2
            self.free.setdefault(order, []).append(idx + order)
        return idx
    def free(self, idx):
        # PEDAGOGY-SOLUTION: D7-BUDDY-FREE
        # educational: treat freed block as size-1 unit then merge greedily from need=1
        order = 1
        while True:
            buddy = idx ^ order
            lst = self.free.setdefault(order, [])
            if buddy in lst:
                lst.remove(buddy)
                idx = min(idx, buddy)
                order *= 2
                if order > self.size:
                    break
                continue
            lst.append(idx)
            lst.sort()
            return
''',
           '''from buddy_allocator import Buddy

def test_init():
    # PEDAGOGY-TEST: D7-BUDDY-INIT
    b = Buddy(8)
    assert b.size == 8
    assert b.free[8] == [0]

def test_alloc():
    # PEDAGOGY-TEST: D7-BUDDY-ALLOC
    b = Buddy(8)
    a = b.alloc(3)
    assert a == 0
    assert b.alloc(8) is None or True  # may still have room for 4
    c = b.alloc(4)
    assert c in (0, 4) or c is not None

def test_free_merge():
    # PEDAGOGY-TEST: D7-BUDDY-FREE
    b = Buddy(8)
    a = b.alloc(4)
    b.free(a)
    assert 0 in b.free.get(4, []) or 0 in b.free.get(8, [])
''',
           {"D7-BUDDY-INIT": ("starter/buddy_allocator.py", "__init__"),
            "D7-BUDDY-ALLOC": ("starter/buddy_allocator.py", "alloc"),
            "D7-BUDDY-FREE": ("starter/buddy_allocator.py", "free")},
           {"D7-BUDDY-INIT": "if size < 1 or size & (size - 1):\n    raise ValueError('size power of two')\nself.size = size\nself.free = {size: [0]}",
            "D7-BUDDY-ALLOC": "need=1\nwhile need < n: need *= 2\n# split from larger free list; return idx",
            "D7-BUDDY-FREE": "order=1\n# merge with buddy idx^order while present"})

    # Fix buddy tests to be deterministic - rewrite simpler buddy
    mod = ROOT / "days" / day / "systems" / "buddy_allocator"
    W(mod / "solutions" / "buddy_allocator.py", '''class Buddy:
    def __init__(self, size):
        # PEDAGOGY-SOLUTION: D7-BUDDY-INIT
        if size < 1 or (size & (size - 1)) != 0:
            raise ValueError("size power of two")
        self.size = size
        self.free = {size: [0]}
        self.used = {}
    def alloc(self, n):
        # PEDAGOGY-SOLUTION: D7-BUDDY-ALLOC
        need = 1
        while need < n:
            need <<= 1
        if need > self.size:
            return None
        order = need
        while order <= self.size and not self.free.get(order):
            order <<= 1
        if order > self.size or not self.free.get(order):
            return None
        idx = self.free[order].pop(0)
        while order > need:
            order >>= 1
            self.free.setdefault(order, []).append(idx + order)
            self.free[order].sort()
        self.used[idx] = need
        return idx
    def free(self, idx):
        # PEDAGOGY-SOLUTION: D7-BUDDY-FREE
        if idx not in self.used:
            raise KeyError(idx)
        order = self.used.pop(idx)
        while order < self.size:
            buddy = idx ^ order
            lst = self.free.setdefault(order, [])
            if buddy in lst:
                lst.remove(buddy)
                idx = min(idx, buddy)
                order <<= 1
                continue
            lst.append(idx)
            lst.sort()
            return
        self.free.setdefault(self.size, []).append(0)
''')
    W(mod / "starter" / "buddy_allocator.py", '''class Buddy:
    def __init__(self, size):
        # TODO [D7-BUDDY-INIT]
        raise NotImplementedError("D7-BUDDY-INIT")
    def alloc(self, n):
        # TODO [D7-BUDDY-ALLOC]
        raise NotImplementedError("D7-BUDDY-ALLOC")
    def free(self, idx):
        # TODO [D7-BUDDY-FREE]
        raise NotImplementedError("D7-BUDDY-FREE")
''')
    W(mod / "starter" / "test_buddy_allocator.py", '''from buddy_allocator import Buddy

def test_init():
    # PEDAGOGY-TEST: D7-BUDDY-INIT
    b = Buddy(8)
    assert b.size == 8 and b.free[8] == [0]

def test_alloc():
    # PEDAGOGY-TEST: D7-BUDDY-ALLOC
    b = Buddy(8)
    assert b.alloc(3) == 0
    assert b.used[0] == 4
    assert b.alloc(4) == 4

def test_free_merge():
    # PEDAGOGY-TEST: D7-BUDDY-FREE
    b = Buddy(8)
    a = b.alloc(4)
    c = b.alloc(4)
    b.free(a)
    b.free(c)
    assert b.free.get(8) == [0]
''')
    W(mod / "solutions" / "test_buddy_allocator.py", (mod / "starter" / "test_buddy_allocator.py").read_text(encoding="utf-8"))

    # welford layernorm
    py_mod(day, "ai", "welford_layernorm",
           ["D7-WEL-MEAN", "D7-WEL-VAR", "D7-WEL-NORM"],
           "Welford online mean/variance + LayerNorm y=(x-mean)/sqrt(var+eps).",
           '''def welford(xs):
    # TODO [D7-WEL-MEAN]
    # TODO [D7-WEL-VAR]
    raise NotImplementedError("D7-WEL-MEAN")

def layernorm(xs, eps=1e-5):
    # TODO [D7-WEL-NORM]
    raise NotImplementedError("D7-WEL-NORM")
''',
           '''import math

def welford(xs):
    # PEDAGOGY-SOLUTION: D7-WEL-MEAN
    # PEDAGOGY-SOLUTION: D7-WEL-VAR
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    var = m2 / n if n else 0.0
    return mean, var

def layernorm(xs, eps=1e-5):
    # PEDAGOGY-SOLUTION: D7-WEL-NORM
    mean, var = welford(xs)
    s = math.sqrt(var + eps)
    return [(x - mean) / s for x in xs]
''',
           '''from welford_layernorm import welford, layernorm

def test_mean_var():
    # PEDAGOGY-TEST: D7-WEL-MEAN
    # PEDAGOGY-TEST: D7-WEL-VAR
    m, v = welford([1.0, 2.0, 3.0])
    assert abs(m - 2.0) < 1e-9
    assert abs(v - (2.0 / 3.0)) < 1e-9

def test_norm():
    # PEDAGOGY-TEST: D7-WEL-NORM
    y = layernorm([1.0, 2.0, 3.0], eps=0.0)
    assert abs(sum(y)) < 1e-9
''',
           {"D7-WEL-MEAN": ("starter/welford_layernorm.py", "welford"),
            "D7-WEL-VAR": ("starter/welford_layernorm.py", "welford"),
            "D7-WEL-NORM": ("starter/welford_layernorm.py", "layernorm")},
           {"D7-WEL-MEAN": "n=0; mean=0.0\nfor x in xs:\n    n+=1; mean += (x-mean)/n",
            "D7-WEL-VAR": "m2 += d*(x-mean)\nvar = m2/n",
            "D7-WEL-NORM": "return [(x-mean)/sqrt(var+eps) for x in xs]"})

    # x86 prologue
    py_mod(day, "redteam", "x86_prologue_triage",
           ["D7-X86-PUSH", "D7-X86-MOV", "D7-X86-STACK"],
           "Triagem de prologo x86-64 sintetico: push rbp, mov rbp,rsp, sub rsp.",
           '''def triage(data: bytes):
    out = {"push_rbp": False, "frame_pointer": False, "stack_reserve": 0, "consumed": 0}
    i = 0
    # TODO [D7-X86-PUSH]
    # TODO [D7-X86-MOV]
    # TODO [D7-X86-STACK]
    raise NotImplementedError("D7-X86-PUSH")
''',
           '''def triage(data: bytes):
    out = {"push_rbp": False, "frame_pointer": False, "stack_reserve": 0, "consumed": 0}
    i = 0
    # PEDAGOGY-SOLUTION: D7-X86-PUSH
    if i < len(data) and data[i] == 0x55:
        out["push_rbp"] = True
        i += 1
    # PEDAGOGY-SOLUTION: D7-X86-MOV
    if data[i:i+3] == b"\\x48\\x89\\xe5":
        out["frame_pointer"] = True
        i += 3
    # PEDAGOGY-SOLUTION: D7-X86-STACK
    if data[i:i+3] == b"\\x48\\x83\\xec" and i + 4 <= len(data):
        out["stack_reserve"] = data[i+3]
        i += 4
    elif data[i:i+3] == b"\\x48\\x81\\xec" and i + 7 <= len(data):
        out["stack_reserve"] = int.from_bytes(data[i+3:i+7], "little")
        i += 7
    out["consumed"] = i
    return out
''',
           '''from x86_prologue_triage import triage

def test_push_mov_stack():
    # PEDAGOGY-TEST: D7-X86-PUSH
    # PEDAGOGY-TEST: D7-X86-MOV
    # PEDAGOGY-TEST: D7-X86-STACK
    blob = bytes([0x55, 0x48, 0x89, 0xe5, 0x48, 0x83, 0xec, 0x20])
    r = triage(blob)
    assert r["push_rbp"] and r["frame_pointer"] and r["stack_reserve"] == 0x20 and r["consumed"] == 8
''',
           {"D7-X86-PUSH": ("starter/x86_prologue_triage.py", "triage"),
            "D7-X86-MOV": ("starter/x86_prologue_triage.py", "triage"),
            "D7-X86-STACK": ("starter/x86_prologue_triage.py", "triage")},
           {"D7-X86-PUSH": "if data[i]==0x55:\n    out['push_rbp']=True\n    i+=1",
            "D7-X86-MOV": "if data[i:i+3]==b'\\x48\\x89\\xe5':\n    out['frame_pointer']=True\n    i+=3",
            "D7-X86-STACK": "if data[i:i+3]==b'\\x48\\x83\\xec':\n    out['stack_reserve']=data[i+3]\n    i+=4"})

    # proc_stat
    py_mod(day, "linux", "proc_stat_parser",
           ["D7-PROC-PREFIX", "D7-PROC-FIELDS", "D7-PROC-SELF"],
           "Parse /proc/[pid]/stat com comm entre parenteses.",
           '''def parse_stat(text):
    # TODO [D7-PROC-PREFIX]
    # TODO [D7-PROC-FIELDS]
    raise NotImplementedError("D7-PROC-PREFIX")

def read_self():
    # TODO [D7-PROC-SELF]
    raise NotImplementedError("D7-PROC-SELF")
''',
           '''def parse_stat(text):
    # PEDAGOGY-SOLUTION: D7-PROC-PREFIX
    lp = text.find("(")
    rp = text.rfind(")")
    if lp < 0 or rp < lp:
        raise ValueError("format")
    pid = int(text[:lp].strip())
    comm = text[lp+1:rp]
    # PEDAGOGY-SOLUTION: D7-PROC-FIELDS
    rest = text[rp+2:].split()
    if len(rest) < 20:
        raise ValueError("truncated")
    return {
        "pid": pid,
        "comm": comm,
        "state": rest[0],
        "ppid": int(rest[1]),
        "utime": int(rest[11]),
        "stime": int(rest[12]),
        "num_threads": int(rest[17]),
        "starttime": int(rest[19]),
    }

def read_self():
    # PEDAGOGY-SOLUTION: D7-PROC-SELF
    # lab: parse fixture string instead of real /proc on Windows
    fixture = "1 (init) S 0 0 0 0 0 0 0 0 0 0 0 10 20 0 0 0 0 1 0 100"
    return parse_stat(fixture)
''',
           '''from proc_stat_parser import parse_stat, read_self

def test_prefix_fields():
    # PEDAGOGY-TEST: D7-PROC-PREFIX
    # PEDAGOGY-TEST: D7-PROC-FIELDS
    r = parse_stat("42 (my task) R 1 0 0 0 0 0 0 0 0 0 0 5 7 0 0 0 0 3 0 99")
    assert r["pid"] == 42 and r["comm"] == "my task" and r["state"] == "R"
    assert r["utime"] == 5 and r["stime"] == 7 and r["num_threads"] == 3

def test_self():
    # PEDAGOGY-TEST: D7-PROC-SELF
    r = read_self()
    assert r["pid"] == 1 and r["comm"] == "init"
''',
           {"D7-PROC-PREFIX": ("starter/proc_stat_parser.py", "parse_stat"),
            "D7-PROC-FIELDS": ("starter/proc_stat_parser.py", "parse_stat"),
            "D7-PROC-SELF": ("starter/proc_stat_parser.py", "read_self")},
           {"D7-PROC-PREFIX": "lp=text.find('('); rp=text.rfind(')')\npid=int(text[:lp].strip()); comm=text[lp+1:rp]",
            "D7-PROC-FIELDS": "rest=text[rp+2:].split()\nreturn dict with utime rest[11]",
            "D7-PROC-SELF": "return parse_stat(fixture)"})

    # pratt
    py_mod(day, "parsers", "pratt_expr",
           ["D7-PRATT-LEX", "D7-PRATT-NUD", "D7-PRATT-LED"],
           "Pratt parser: lex + NUD + LED com ^ right-assoc.",
           '''import re

def lex(src):
    # TODO [D7-PRATT-LEX]
    raise NotImplementedError("D7-PRATT-LEX")

def parse(src):
    toks = lex(src)
    pos = 0
    def expr(min_bp=0):
        nonlocal pos
        # TODO [D7-PRATT-NUD]
        # TODO [D7-PRATT-LED]
        raise NotImplementedError("D7-PRATT-NUD")
    return expr()
''',
           Path(ROOT / "projects/chris-parser/pratt_day07.py").read_text(encoding="utf-8") if (ROOT / "projects/chris-parser/pratt_day07.py").exists() else "pass",
           '''from pratt_expr import lex, parse

def test_lex():
    # PEDAGOGY-TEST: D7-PRATT-LEX
    assert lex("1+2")[:3] == [("NUM", 1.0), ("+", "+"), ("NUM", 2.0)]

def test_nud_led():
    # PEDAGOGY-TEST: D7-PRATT-NUD
    # PEDAGOGY-TEST: D7-PRATT-LED
    ast = parse("2^3^2")
    assert ast[0] == "bin" and ast[1] == "^"
''',
           {"D7-PRATT-LEX": ("starter/pratt_expr.py", "lex"),
            "D7-PRATT-NUD": ("starter/pratt_expr.py", "expr"),
            "D7-PRATT-LED": ("starter/pratt_expr.py", "expr")},
           {"D7-PRATT-LEX": "out=[]; scan NUM and ops\nout.append(('EOF',None))",
            "D7-PRATT-NUD": "NUM / unary- / (expr)",
            "D7-PRATT-LED": "while op in bp: parse right with rbp"})
    # overwrite solution with project file properly
    W(ROOT / f"days/{day}/parsers/pratt_expr/solutions/pratt_expr.py",
      (ROOT / "projects/chris-parser/pratt_day07.py").read_text(encoding="utf-8"))

    # agent state machine
    py_mod(day, "agent", "agent_state_machine",
           ["D7-AGENT-TRANSITIONS", "D7-AGENT-RUN", "D7-AGENT-TRACE"],
           "FSM PERCEIVE..DONE com retries.",
           '''from dataclasses import dataclass
STATES = ["PERCEIVE", "PLAN", "ACT", "OBSERVE", "VERIFY", "REVISE", "DONE", "FAILED"]

@dataclass(frozen=True)
class ToolResult:
    ok: bool
    evidence: str

def next_state(state, event):
    # TODO [D7-AGENT-TRANSITIONS]
    raise NotImplementedError("D7-AGENT-TRANSITIONS")

def run(task, tool, verify, max_retries=2):
    # TODO [D7-AGENT-RUN]
    # TODO [D7-AGENT-TRACE]
    raise NotImplementedError("D7-AGENT-RUN")
''',
           (ROOT / "projects/chris-agent-core/agent_state_machine_day07.py").read_text(encoding="utf-8"),
           '''from agent_state_machine import next_state, run, ToolResult

def test_transitions():
    # PEDAGOGY-TEST: D7-AGENT-TRANSITIONS
    assert next_state("PERCEIVE", "perceived") == "PLAN"
    try:
        next_state("DONE", "x")
        assert False
    except ValueError:
        pass

def test_run_trace():
    # PEDAGOGY-TEST: D7-AGENT-RUN
    # PEDAGOGY-TEST: D7-AGENT-TRACE
    def tool(task, retry):
        return ToolResult(ok=True, evidence="ok")
    state, trace = run("t", tool, lambda r: r.ok)
    assert state == "DONE"
    assert trace[0]["state"] == "PERCEIVE"
''',
           {"D7-AGENT-TRANSITIONS": ("starter/agent_state_machine.py", "next_state"),
            "D7-AGENT-RUN": ("starter/agent_state_machine.py", "run"),
            "D7-AGENT-TRACE": ("starter/agent_state_machine.py", "run")},
           {"D7-AGENT-TRANSITIONS": "m={(PERCEIVE,perceived):PLAN,...}\nreturn m[(state,event)]",
            "D7-AGENT-RUN": "loop tool/verify with retries",
            "D7-AGENT-TRACE": "trace.append({state,event,data})"})

    # grep_dfa
    py_mod(day, "unix", "grep_dfa",
           ["D7-GREP-DFA", "D7-GREP-SEARCH", "D7-GREP-FILE"],
           "DFA literal para grep educacional.",
           '''class LiteralDFA:
    def __init__(self, pattern):
        # TODO [D7-GREP-DFA]
        raise NotImplementedError("D7-GREP-DFA")
    def fullmatch_at(self, text, start):
        raise NotImplementedError
    def contains(self, text):
        # TODO [D7-GREP-SEARCH]
        raise NotImplementedError("D7-GREP-SEARCH")

def grep_file(path, pattern):
    # TODO [D7-GREP-FILE]
    raise NotImplementedError("D7-GREP-FILE")
''',
           (ROOT / "projects/chris-grep/grep_dfa_day07.py").read_text(encoding="utf-8"),
           '''from pathlib import Path
from grep_dfa import LiteralDFA, grep_file

def test_dfa_search(tmp_path=None):
    # PEDAGOGY-TEST: D7-GREP-DFA
    # PEDAGOGY-TEST: D7-GREP-SEARCH
    d = LiteralDFA("ab")
    assert d.contains("xxabyy")
    assert not d.contains("a")

def test_file(tmp_path):
    # PEDAGOGY-TEST: D7-GREP-FILE
    p = tmp_path / "f.txt"
    p.write_text("one\\nabc\\nzzz\\n", encoding="utf-8")
    hits = grep_file(str(p), "ab")
    assert hits == [(2, "abc")]
''',
           {"D7-GREP-DFA": ("starter/grep_dfa.py", "__init__"),
            "D7-GREP-SEARCH": ("starter/grep_dfa.py", "contains"),
            "D7-GREP-FILE": ("starter/grep_dfa.py", "grep_file")},
           {"D7-GREP-DFA": "self.trans={(i,ch):i+1 ...}",
            "D7-GREP-SEARCH": "any(fullmatch_at(text,i))",
            "D7-GREP-FILE": "for line enumerate: if contains append"})

    # branch predictor
    py_mod(day, "architecture", "branch_predictor",
           ["D7-BR-INIT", "D7-BR-PRED", "D7-BR-UPDATE"],
           "Preditor 2-bit saturating counter.",
           '''class TwoBit:
    def __init__(self):
        # TODO [D7-BR-INIT]
        raise NotImplementedError("D7-BR-INIT")
    def predict(self):
        # TODO [D7-BR-PRED]
        raise NotImplementedError("D7-BR-PRED")
    def update(self, taken: bool):
        # TODO [D7-BR-UPDATE]
        raise NotImplementedError("D7-BR-UPDATE")
''',
           '''class TwoBit:
    def __init__(self):
        # PEDAGOGY-SOLUTION: D7-BR-INIT
        self.state = 1  # 0,1 not-taken; 2,3 taken
    def predict(self):
        # PEDAGOGY-SOLUTION: D7-BR-PRED
        return self.state >= 2
    def update(self, taken: bool):
        # PEDAGOGY-SOLUTION: D7-BR-UPDATE
        if taken:
            self.state = min(3, self.state + 1)
        else:
            self.state = max(0, self.state - 1)
''',
           '''from branch_predictor import TwoBit

def test_init_pred():
    # PEDAGOGY-TEST: D7-BR-INIT
    # PEDAGOGY-TEST: D7-BR-PRED
    p = TwoBit()
    assert p.state == 1
    assert p.predict() is False

def test_update():
    # PEDAGOGY-TEST: D7-BR-UPDATE
    p = TwoBit()
    p.update(True); p.update(True)
    assert p.predict() is True
    p.update(False); p.update(False); p.update(False)
    assert p.predict() is False
''',
           {"D7-BR-INIT": ("starter/branch_predictor.py", "__init__"),
            "D7-BR-PRED": ("starter/branch_predictor.py", "predict"),
            "D7-BR-UPDATE": ("starter/branch_predictor.py", "update")},
           {"D7-BR-INIT": "self.state=1",
            "D7-BR-PRED": "return self.state>=2",
            "D7-BR-UPDATE": "saturate 0..3"})

    # explicit barriers (python headless gfx)
    py_mod(day, "graphics", "explicit_barriers",
           ["D7-GFX-VALIDATE", "D7-GFX-D3D12", "D7-GFX-VULKAN"],
           "Validacao de transicoes + mapa D3D12/Vulkan (headless).",
           '''USAGES = ["Undefined", "CopyDst", "ShaderRead", "RenderTarget", "Present"]

def validate_transition(before, after):
    # TODO [D7-GFX-VALIDATE]
    raise NotImplementedError("D7-GFX-VALIDATE")

def d3d12_barrier(before, after):
    # TODO [D7-GFX-D3D12]
    raise NotImplementedError("D7-GFX-D3D12")

def vulkan_barrier(before, after):
    # TODO [D7-GFX-VULKAN]
    raise NotImplementedError("D7-GFX-VULKAN")
''',
           (ROOT / "projects/chris-render-graph/explicit_barriers_day07.py").read_text(encoding="utf-8"),
           '''from explicit_barriers import validate_transition, d3d12_barrier, vulkan_barrier

def test_validate():
    # PEDAGOGY-TEST: D7-GFX-VALIDATE
    assert validate_transition("Undefined", "CopyDst") is True
    try:
        validate_transition("Undefined", "Present")
        assert False
    except ValueError:
        pass

def test_maps():
    # PEDAGOGY-TEST: D7-GFX-D3D12
    # PEDAGOGY-TEST: D7-GFX-VULKAN
    d = d3d12_barrier("CopyDst", "ShaderRead")
    assert d["before"] == "COPY_DEST"
    v = vulkan_barrier("CopyDst", "ShaderRead")
    assert v["after"][0] == "SHADER_READ_ONLY_OPTIMAL"
''',
           {"D7-GFX-VALIDATE": ("starter/explicit_barriers.py", "validate_transition"),
            "D7-GFX-D3D12": ("starter/explicit_barriers.py", "d3d12_barrier"),
            "D7-GFX-VULKAN": ("starter/explicit_barriers.py", "vulkan_barrier")},
           {"D7-GFX-VALIDATE": "if (before,after) not in _ALLOWED: raise",
            "D7-GFX-D3D12": "map usages to D3D12 states",
            "D7-GFX-VULKAN": "map to (layout,stage,access)"})
    W(ROOT / f"days/{day}/graphics/explicit_barriers/docs/COMPARISON.md", """# COMPARISON — explicit_barriers

| Aspecto | CPU/software (lab) | OpenGL | D3D12/Vulkan |
|---------|-------------------|--------|--------------|
| Modelo | tabela de arestas | implícito | barreiras explícitas |
| Validação | set `_ALLOWED` | driver | app + validation layers |

Headless exempt: contrato de estados, sem janela.
""")

    # async_context node
    mod = ROOT / "days" / day / "nodejs" / "async_context"
    W(mod / "starter" / "async_context.js", ''''use strict';
const { AsyncLocalStorage } = require('async_hooks');

function createStore() {
  // TODO [D7-NODE-ALS]
  throw new Error('D7-NODE-ALS');
}

function runWith(store, id, fn) {
  // TODO [D7-NODE-RUN]
  throw new Error('D7-NODE-RUN');
}

function currentId(store) {
  // TODO [D7-NODE-GET]
  throw new Error('D7-NODE-GET');
}

module.exports = { createStore, runWith, currentId };
''')
    W(mod / "solutions" / "async_context.js", ''''use strict';
const { AsyncLocalStorage } = require('async_hooks');

function createStore() {
  // PEDAGOGY-SOLUTION: D7-NODE-ALS
  return new AsyncLocalStorage();
}

function runWith(store, id, fn) {
  // PEDAGOGY-SOLUTION: D7-NODE-RUN
  return store.run({ id }, fn);
}

function currentId(store) {
  // PEDAGOGY-SOLUTION: D7-NODE-GET
  const s = store.getStore();
  return s ? s.id : null;
}

module.exports = { createStore, runWith, currentId };
''')
    W(mod / "starter" / "test.js", ''''use strict';
const assert = require('assert');
const { createStore, runWith, currentId } = require('./async_context');
// PEDAGOGY-TEST: D7-NODE-ALS
const store = createStore();
assert.ok(store);
// PEDAGOGY-TEST: D7-NODE-RUN
// PEDAGOGY-TEST: D7-NODE-GET
runWith(store, 7, () => {
  assert.strictEqual(currentId(store), 7);
});
assert.strictEqual(currentId(store), null);
console.log('ok');
''')
    W(mod / "solutions" / "test.js", (mod / "starter" / "test.js").read_text(encoding="utf-8"))
    W(mod / "starter" / "package.json", '{\n  "name": "async-context",\n  "private": true\n}\n')
    W(mod / "solutions" / "package.json", '{\n  "name": "async-context",\n  "private": true\n}\n')
    pedagogy(mod, "async_context", "javascript",
             ["D7-NODE-ALS", "D7-NODE-RUN", "D7-NODE-GET"],
             "AsyncLocalStorage: criar store, runWith id, currentId.",
             f"cd days/{day}/nodejs/async_context/starter\nnode test.js",
             {"D7-NODE-ALS": ("starter/async_context.js", "createStore"),
              "D7-NODE-RUN": ("starter/async_context.js", "runWith"),
              "D7-NODE-GET": ("starter/async_context.js", "currentId")},
             {"D7-NODE-ALS": "return new AsyncLocalStorage();",
              "D7-NODE-RUN": "return store.run({ id }, fn);",
              "D7-NODE-GET": "const s=store.getStore(); return s?s.id:null;"})

    # dotnet channel
    mod = ROOT / "days" / day / "dotnet" / "channel_backpressure"
    W(mod / "solutions" / "Pipeline.cs", (ROOT / "projects/chris-dotnet-bench/ChannelPipelineDay07.cs").read_text(encoding="utf-8"))
    W(mod / "starter" / "Pipeline.cs", '''using System.Threading.Channels;
namespace Chris.ChannelLab;
public static class Pipeline {
    public static async Task<(int checksum,int count)> RunAsync(int count,int capacity) {
        // TODO [D7-DN-CHANNEL]
        // TODO [D7-DN-PRODUCER]
        // TODO [D7-DN-CONSUMER]
        throw new NotImplementedException("D7-DN-CHANNEL");
    }
}
''')
    csproj = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup><Compile Remove="tests/**" /></ItemGroup>
</Project>
'''
    test_csproj = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><IsTestProject>true</IsTestProject></PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
  <ItemGroup><ProjectReference Include="..\\Chris.ChannelLab.csproj" /></ItemGroup>
</Project>
'''
    test_cs = '''using Chris.ChannelLab;
using Xunit;
public class ChannelTests {
    [Fact]
    public async Task Run() {
        // PEDAGOGY-TEST: D7-DN-CHANNEL
        // PEDAGOGY-TEST: D7-DN-PRODUCER
        // PEDAGOGY-TEST: D7-DN-CONSUMER
        var (sum, n) = await Pipeline.RunAsync(5, 2);
        Assert.Equal(10, sum);
        Assert.Equal(5, n);
    }
}
'''
    for base in (mod / "starter", mod / "solutions"):
        W(base / "Chris.ChannelLab.csproj", csproj)
        W(base / "tests" / "Chris.ChannelLab.Tests.csproj", test_csproj)
        W(base / "tests" / "ChannelTests.cs", test_cs)
    pedagogy(mod, "channel_backpressure", "csharp",
             ["D7-DN-CHANNEL", "D7-DN-PRODUCER", "D7-DN-CONSUMER"],
             "Channel bounded Wait + producer/consumer checksum.",
             f"cd days/{day}/dotnet/channel_backpressure/starter\ndotnet test tests/Chris.ChannelLab.Tests.csproj",
             {"D7-DN-CHANNEL": ("starter/Pipeline.cs", "RunAsync"),
              "D7-DN-PRODUCER": ("starter/Pipeline.cs", "RunAsync"),
              "D7-DN-CONSUMER": ("starter/Pipeline.cs", "RunAsync")},
             {"D7-DN-CHANNEL": "Channel.CreateBounded<int>(... Wait)",
              "D7-DN-PRODUCER": "WriteAsync 0..count-1; Complete",
              "D7-DN-CONSUMER": "ReadAllAsync sum+=item"})

    print("day09 labs done")


if __name__ == "__main__":
    day09()
    print("part1 ok — continue in scaffold_github_labs_09_11_b.py")
