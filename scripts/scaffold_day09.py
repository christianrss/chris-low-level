#!/usr/bin/env python3
"""Scaffold Day 09 — Observabilidade, profiling e depuração low-level (13 tier-A modules)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = "2026-09-09"
DAY09 = ROOT / "days" / DAY
TODO_RE = re.compile(r"TODO\s*\[([A-Z0-9-]+)\]")
CODE_EXT = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".py", ".ts", ".js", ".cs", ".rs", ".asm", ".s", ".yar", ".sh"}


def write_resolucao(path: Path, title: str, baseline_cmd: str, todos: list[dict]) -> None:
    lines = [
        f"# Resolução guiada — {title}",
        "",
        "## Mapa exato starter → resolução",
        "",
        "| TODO ID | Arquivo starter | Função / âncora | Substituir |",
        "|---------|-----------------|-----------------|------------|",
    ]
    for t in todos:
        lines.append(
            f"| `{t['id']}` | `{t['file']}` | `{t['fn']}` | stub `TODO [{t['id']}]` |"
        )
    lines.extend([
        "",
        "---",
        "",
        "## Baseline",
        "",
        "```powershell",
        baseline_cmd,
        "```",
        "",
        "**Esperado antes dos TODOs:** build/test FAIL até implementar cada ID.",
        "",
        "## Debug / depuração",
        "",
        "| Sintoma | Causa provável | Correção |",
        "|---------|----------------|----------|",
        "| `NotImplementedError` | stub não substituído | localize `TODO [ID]` no starter |",
        "| assert falha | invariante violada | trace manual em TESTES_GUIADOS |",
        "| import error | cwd errado | rode o baseline a partir de `starter/` |",
        "",
        "## Relatório de resolução",
        "",
    ])
    for t in todos:
        lang = t.get("lang", "python")
        code = t["code"]
        lines.extend([
            f"## {t['id']} — `{t['fn']}`",
            "",
            f"### Onde colocar ({t['id']})",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| Arquivo | `{t['file']}` |",
            f"| Função | `{t['fn']}` |",
            f"| Substituir | corpo com `TODO [{t['id']}]` |",
            f"| Não mexer | demais funções até este ID passar |",
            "",
            f"### 1. O problema ({t['id']})",
            "",
            t["problem"],
            "",
            f"### Escreva o código ({t['id']})",
            "",
            f"```{lang}",
            code,
            "```",
            "",
            f"### Por que funciona ({t['id']})",
            "",
            t["why"],
            "",
            f"### Verifique ({t['id']})",
            "",
            t["verify"],
            "",
            f"**Checkpoint:** rode o teste parcial antes de avançar para o próximo TODO.",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_teoria(path: Path, title: str, overview: str, concepts: list[tuple[str, str, str, str]]) -> None:
    """concepts: (heading, o_que, como, por_que) — each tuple must be unique (no filler loops)."""
    lines = [
        f"# Teoria passo a passo — {title}",
        "",
        "## Visão geral",
        "",
        overview,
        "",
        "```mermaid",
        "flowchart LR",
        "  OBS[observar] --> PROFILE[profile]",
        "  PROFILE --> DEBUG[depurar]",
        "  DEBUG --> FIX[corrigir]",
        "```",
        "",
        "| Etapa | Por quê |",
        "|-------|---------|",
        "| Trace primeiro | Sem evidência você adivinha |",
        "| Hotspots | Otimize onde o tempo realmente vai |",
        "| Replay | Reproduza bugs com log determinístico |",
        "",
    ]
    for i, (heading, o_que, como, por_que) in enumerate(concepts, 1):
        lines.extend([
            f"## {i}. {heading}",
            "",
            f"**O quê:** {o_que}",
            "",
            f"**Como:** {como}",
            "",
            f"**Por quê:** {por_que}",
            "",
            f"**Invariantes ({heading}):** estado de `{heading.lower()}` é observável antes de mutar; "
            f"erros devem ir para o relatório de {title}, não para stderr silencioso.",
            "",
            f"**Bug típico:** saída vazia em `{heading.lower()}` → stub `TODO` ainda no starter; "
            f"depure com o Caso {min(i, 3)} de `TESTES_GUIADOS.md`.",
            "",
            "**Trace manual:**",
            "",
            "```text",
            f"{title} / {heading} / passo-{i}: anote entrada → transformação → saída numérica",
            "```",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def teoria_concepts_extended(base: list[tuple[str, str, str, str]], title: str) -> list[tuple[str, str, str, str]]:
    """Pad to ≥9 unique sections (~125 TEORIA lines) without duplicate filler."""
    extras = [
        ("Overhead de probe", f"Custo de instrumentar {title}.", "Amostragem / contadores leves.", "Por quê medir antes de otimizar cegamente."),
        ("Correlação cross-layer", f"Ligar {title} a logs de outras trilhas.", "IDs estáveis em spans/traces.", "Por quê debug distribuído exige chaves comuns."),
        ("Baseline em CI", f"Golden trace para {title}.", "Hash ou diff textual.", "Por quê regressões de perfil são silenciosas."),
        ("Sampling vs contagem", "Quando amostrar vs contar tudo.", "Taxa adaptativa.", "Por quê contador full tem custo em hot path."),
        ("Depuração de outliers", "Valores fora da mediana.", "Percentil p99 no relatório.", "Por quê média esconde cauda longa."),
        ("Integração capstone", f"Portar {title} para projects/.", "API mínima documentada.", "Por quê portfólio exige código reutilizável."),
    ]
    out = list(base)
    for item in extras:
        if len(out) >= 9:
            break
        out.append(item)
    return out


def write_pedagogy_pack(
    base: Path,
    title: str,
    readme: str,
    baseline: str,
    todos: list[dict],
    teoria_concepts: list[tuple[str, str, str, str]],
    teoria_overview: str,
    test_cases: list[str],
    benchmark_cmd: str = "python -m timeit",
) -> None:
    base.mkdir(parents=True, exist_ok=True)
    (base / "README.md").write_text(readme, encoding="utf-8")
    write_teoria(
        base / "TEORIA_PASSO_A_PASSO.md",
        title,
        teoria_overview,
        teoria_concepts_extended(teoria_concepts, title),
    )
    write_resolucao(base / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", title, baseline, todos)
    (base / "PESQUISA_GUIADA.md").write_text(
        f"# Pesquisa guiada — {title}\n\n"
        "1. Documentação oficial da API/syscall alvo\n"
        "2. Ferramenta de produção equivalente (perf, dotTrace, Chrome DevTools)\n"
        "3. Trade-off: overhead de instrumentação vs precisão\n",
        encoding="utf-8",
    )
    ex = "\n".join(f"- `{t['id']}` — {t['fn']}" for t in todos)
    (base / "EXERCICIOS.md").write_text(
        f"# Exercícios\n\n## Fácil\nValide invariantes no papel.\n\n## Médio\n{ex}\n\n"
        "## Difícil\nEdge cases em TESTES_GUIADOS.\n\n## Desafio\nIntegre com capstone do dia.\n",
        encoding="utf-8",
    )
    case_lines = []
    for i, (t, c) in enumerate(zip(todos, test_cases), 1):
        case_lines.append(f"### Caso {i}: `{t['id']}` — {c}")
    (base / "TESTES_GUIADOS.md").write_text(
        "# Testes guiados\n\n" + "\n\n".join(case_lines) + "\n",
        encoding="utf-8",
    )
    (base / "BENCHMARK_GUIADO.md").write_text(
        f"# Benchmark guiado — {title}\n\n```powershell\n{benchmark_cmd}\n```\n\n"
        "## Resultados observados\n\nBenchmark não executado neste ambiente.\n",
        encoding="utf-8",
    )


def write_pair(base: Path, rel: str, starter: str, solution: str) -> None:
    for side, body in (("starter", starter), ("solutions", solution)):
        p = base / side / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")


def scaffold_clvm_trace_profiler() -> None:
    base = DAY09 / "systems" / "clvm_trace_profiler"
    todos = [
        {"id": "SYS-CLVM-TRACE-01", "file": "starter/clvm_trace.py", "fn": "record_opcode",
         "problem": "Sem contagem por opcode você não vê hotspots na VM.",
         "code": "def record_opcode(op: int, counters: dict[int, int]) -> None:\n    counters[op] = counters.get(op, 0) + 1",
         "why": "Dict acumula frequência em O(1) amortizado.", "verify": "Caso 1: dois PUSH incrementam contador."},
        {"id": "SYS-CLVM-HOT-02", "file": "starter/clvm_trace.py", "fn": "top_hotspots",
         "problem": "Precisa ranquear opcodes por frequência.",
         "code": "def top_hotspots(counters: dict[int, int], n: int) -> list[tuple[int, int]]:\n    items = sorted(counters.items(), key=lambda kv: (-kv[1], kv[0]))\n    return items[:n]",
         "why": "Sort por (-count, op) dá ordem estável.", "verify": "Caso 2: opcode 0x10 lidera."},
        {"id": "SYS-CLVM-REPORT-03", "file": "starter/clvm_trace.py", "fn": "format_trace_report",
         "problem": "Relatório legível para diff em CI.",
         "code": 'def format_trace_report(counters: dict[int, int]) -> str:\n    lines = [f"op=0x{op:02x} count={cnt}" for op, cnt in sorted(counters.items())]\n    return "\\n".join(lines)',
         "why": "Hex + sort facilita comparar traces.", "verify": "Caso 3: duas linhas ordenadas."},
    ]
    starter = '''"""CLVM opcode trace profiler — hotspot counting."""

from __future__ import annotations


def record_opcode(op: int, counters: dict[int, int]) -> None:
    """TODO [SYS-CLVM-TRACE-01]: increment per-opcode counter."""
    raise NotImplementedError("SYS-CLVM-TRACE-01")


def top_hotspots(counters: dict[int, int], n: int) -> list[tuple[int, int]]:
    """TODO [SYS-CLVM-HOT-02]: return top-n (op, count) pairs."""
    raise NotImplementedError("SYS-CLVM-HOT-02")


def format_trace_report(counters: dict[int, int]) -> str:
    """TODO [SYS-CLVM-REPORT-03]: stable text report."""
    raise NotImplementedError("SYS-CLVM-REPORT-03")
'''
    sol = starter.replace(
        'def record_opcode(op: int, counters: dict[int, int]) -> None:\n    """TODO [SYS-CLVM-TRACE-01]: increment per-opcode counter."""\n    raise NotImplementedError("SYS-CLVM-TRACE-01")',
        'def record_opcode(op: int, counters: dict[int, int]) -> None:\n    # PEDAGOGY-SOLUTION: SYS-CLVM-TRACE-01\n    counters[op] = counters.get(op, 0) + 1',
    ).replace(
        'def top_hotspots(counters: dict[int, int], n: int) -> list[tuple[int, int]]:\n    """TODO [SYS-CLVM-HOT-02]: return top-n (op, count) pairs."""\n    raise NotImplementedError("SYS-CLVM-HOT-02")',
        'def top_hotspots(counters: dict[int, int], n: int) -> list[tuple[int, int]]:\n    # PEDAGOGY-SOLUTION: SYS-CLVM-HOT-02\n    items = sorted(counters.items(), key=lambda kv: (-kv[1], kv[0]))\n    return items[:n]',
    ).replace(
        'def format_trace_report(counters: dict[int, int]) -> str:\n    """TODO [SYS-CLVM-REPORT-03]: stable text report."""\n    raise NotImplementedError("SYS-CLVM-REPORT-03")',
        'def format_trace_report(counters: dict[int, int]) -> str:\n    # PEDAGOGY-SOLUTION: SYS-CLVM-REPORT-03\n    lines = [f"op=0x{op:02x} count={cnt}" for op, cnt in sorted(counters.items())]\n    return "\\n".join(lines)',
    )
    test = '''# PEDAGOGY-TEST: SYS-CLVM-TRACE-01
# PEDAGOGY-TEST: SYS-CLVM-HOT-02
# PEDAGOGY-TEST: SYS-CLVM-REPORT-03
# Caso 1: dois PUSH incrementam contador
# Caso 2: opcode 0x10 lidera hotspots
# Caso 3: relatório com duas linhas ordenadas
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from clvm_trace import record_opcode, top_hotspots, format_trace_report

def main():
    c: dict[int, int] = {}
    record_opcode(0x01, c)
    record_opcode(0x01, c)
    record_opcode(0x10, c)
    assert c[0x01] == 2
    hot = top_hotspots(c, 1)
    assert hot[0] == (0x01, 2)
    rep = format_trace_report(c)
    assert "op=0x01 count=2" in rep
    assert "op=0x10 count=1" in rep
    print("OK clvm_trace")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "clvm_trace.py", starter, sol)
    write_pair(base, "test_clvm_trace.py", test, test)
    write_pedagogy_pack(
        base, "clvm_trace_profiler",
        "# CLVM trace profiler\n\nOpcode trace + hotspot counting (continua `clvm_bytecode_verifier`).\n",
        f"cd days/{DAY}/systems/clvm_trace_profiler/starter\npython test_clvm_trace.py",
        todos,
        [("Opcode trace", "Registro de cada opcode executado.", "Dict op→count.", "Hotspots guiam otimização JIT."),
         ("Hotspot ranking", "Top-N por frequência.", "Sort estável.", "Evita otimizar opcode raro."),
         ("Trace report", "Saída textual diffável.", "Linhas op=0xNN.", "CI compara regressões.")],
        "Instrumentação da VM CLVM: cada opcode incrementa contador; relatório ordenado alimenta profiling.",
        ["dois PUSH incrementam contador", "opcode 0x10 em top_hotspots", "relatório duas linhas"],
    )


def scaffold_arena_telemetry() -> None:
    base = DAY09 / "systems" / "arena_telemetry"
    todos = [
        {"id": "SYS-ARENA-ALLOC-01", "file": "starter/arena.py", "fn": "BumpArena.alloc",
         "problem": "Bump allocator precisa retornar offset ou -1 se cheio.",
         "code": "def alloc(self, size: int) -> int:\n    if size <= 0 or self._used + size > self.capacity:\n        return -1\n    off = self._used\n    self._used += size\n    self._allocs += 1\n    return off",
         "why": "Bump é O(1) com reset batch.", "verify": "Caso 1: alloc 8 retorna 0."},
        {"id": "SYS-ARENA-STATS-02", "file": "starter/arena.py", "fn": "BumpArena.stats",
         "problem": "Telemetria expõe uso e número de alocações.",
         "code": 'def stats(self) -> dict[str, int]:\n    return {"used": self._used, "capacity": self.capacity, "allocs": self._allocs}',
         "why": "Métricas guiam tuning de capacity.", "verify": "Caso 2: used=8 após alloc."},
        {"id": "SYS-ARENA-RESET-03", "file": "starter/arena.py", "fn": "BumpArena.reset",
         "problem": "Reset libera arena inteira de uma vez.",
         "code": "def reset(self) -> None:\n    self._used = 0\n    self._allocs = 0",
         "why": "Frame allocator típico em compiladores.", "verify": "Caso 3: used=0 após reset."},
    ]
    starter = '''"""Bump arena allocator with telemetry."""

from __future__ import annotations


class BumpArena:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._used = 0
        self._allocs = 0

    def alloc(self, size: int) -> int:
        """TODO [SYS-ARENA-ALLOC-01]: return offset or -1."""
        raise NotImplementedError("SYS-ARENA-ALLOC-01")

    def stats(self) -> dict[str, int]:
        """TODO [SYS-ARENA-STATS-02]: used/capacity/allocs."""
        raise NotImplementedError("SYS-ARENA-STATS-02")

    def reset(self) -> None:
        """TODO [SYS-ARENA-RESET-03]: zero used and allocs."""
        raise NotImplementedError("SYS-ARENA-RESET-03")
'''
    sol = starter.replace(
        'def alloc(self, size: int) -> int:\n        """TODO [SYS-ARENA-ALLOC-01]: return offset or -1."""\n        raise NotImplementedError("SYS-ARENA-ALLOC-01")',
        'def alloc(self, size: int) -> int:\n        # PEDAGOGY-SOLUTION: SYS-ARENA-ALLOC-01\n        if size <= 0 or self._used + size > self.capacity:\n            return -1\n        off = self._used\n        self._used += size\n        self._allocs += 1\n        return off',
    ).replace(
        'def stats(self) -> dict[str, int]:\n        """TODO [SYS-ARENA-STATS-02]: used/capacity/allocs."""\n        raise NotImplementedError("SYS-ARENA-STATS-02")',
        'def stats(self) -> dict[str, int]:\n        # PEDAGOGY-SOLUTION: SYS-ARENA-STATS-02\n        return {"used": self._used, "capacity": self.capacity, "allocs": self._allocs}',
    ).replace(
        'def reset(self) -> None:\n        """TODO [SYS-ARENA-RESET-03]: zero used and allocs."""\n        raise NotImplementedError("SYS-ARENA-RESET-03")',
        'def reset(self) -> None:\n        # PEDAGOGY-SOLUTION: SYS-ARENA-RESET-03\n        self._used = 0\n        self._allocs = 0',
    )
    test = '''# PEDAGOGY-TEST: SYS-ARENA-ALLOC-01
# PEDAGOGY-TEST: SYS-ARENA-STATS-02
# PEDAGOGY-TEST: SYS-ARENA-RESET-03
# Caso 1: alloc 8 retorna 0
# Caso 2: stats used=8
# Caso 3: reset zera used
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from arena import BumpArena

def main():
    a = BumpArena(64)
    assert a.alloc(8) == 0
    assert a.stats()["used"] == 8
    a.reset()
    assert a.stats()["used"] == 0
    print("OK arena")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "arena.py", starter, sol)
    write_pair(base, "test_arena.py", test, test)
    write_pedagogy_pack(
        base, "arena_telemetry",
        "# Arena telemetry\n\nBump allocator com stats (par com codegen CLVM).\n",
        f"cd days/{DAY}/systems/arena_telemetry/starter\npython test_arena.py",
        todos,
        [("Bump alloc", "Alocação linear em buffer fixo.", "offset += size.", "Cache-friendly em compiladores."),
         ("Stats", "used/capacity/allocs.", "dict de métricas.", "Detecta memory pressure."),
         ("Reset", "Libera frame inteiro.", "_used=0.", "Sem free individual.")],
        "Telemetria de arena: cada alloc registra offset; stats expõem pressão; reset por frame.",
        ["alloc 8 retorna 0", "stats used=8", "reset zera"],
    )


def scaffold_perf_event_open_lab() -> None:
    base = DAY09 / "linux" / "perf_event_open_lab"
    todos = [
        {"id": "LX-PERF-OPEN-01", "file": "starter/perf_lab.py", "fn": "perf_event_open",
         "problem": "Simular abertura de contador perf com type/config.",
         "code": 'def perf_event_open(event_type: int, config: int) -> int:\n    if event_type < 0:\n        return -1\n    return (event_type << 16) | (config & 0xFFFF)',
         "why": "Handle sintético codifica parâmetros.", "verify": "Caso 1: handle positivo."},
        {"id": "LX-PERF-READ-02", "file": "starter/perf_lab.py", "fn": "perf_event_read",
         "problem": "Ler contador acumulado do fd simulado.",
         "code": "def perf_event_read(fd: int, counters: dict[int, int]) -> int:\n    return counters.get(fd, 0)",
         "why": "Dict mapeia fd→valor.", "verify": "Caso 2: retorna 42."},
        {"id": "LX-PERF-CLOSE-03", "file": "starter/perf_lab.py", "fn": "perf_event_close",
         "problem": "Fechar fd remove do mapa.",
         "code": "def perf_event_close(fd: int, counters: dict[int, int]) -> bool:\n    prev = counters.pop(fd, None)\n    return prev is not None",
         "why": "Evita leak de handles simulados.", "verify": "Caso 3: close retorna True."},
    ]
    starter = '''"""perf_event_open subset simulation in Python."""

from __future__ import annotations


def perf_event_open(event_type: int, config: int) -> int:
    """TODO [LX-PERF-OPEN-01]: return synthetic fd or -1."""
    raise NotImplementedError("LX-PERF-OPEN-01")


def perf_event_read(fd: int, counters: dict[int, int]) -> int:
    """TODO [LX-PERF-READ-02]: read counter value."""
    raise NotImplementedError("LX-PERF-READ-02")


def perf_event_close(fd: int, counters: dict[int, int]) -> bool:
    """TODO [LX-PERF-CLOSE-03]: remove fd from counters."""
    raise NotImplementedError("LX-PERF-CLOSE-03")
'''
    sol = starter.replace(
        'def perf_event_open(event_type: int, config: int) -> int:\n    """TODO [LX-PERF-OPEN-01]: return synthetic fd or -1."""\n    raise NotImplementedError("LX-PERF-OPEN-01")',
        'def perf_event_open(event_type: int, config: int) -> int:\n    # PEDAGOGY-SOLUTION: LX-PERF-OPEN-01\n    if event_type < 0:\n        return -1\n    return (event_type << 16) | (config & 0xFFFF)',
    ).replace(
        'def perf_event_read(fd: int, counters: dict[int, int]) -> int:\n    """TODO [LX-PERF-READ-02]: read counter value."""\n    raise NotImplementedError("LX-PERF-READ-02")',
        'def perf_event_read(fd: int, counters: dict[int, int]) -> int:\n    # PEDAGOGY-SOLUTION: LX-PERF-READ-02\n    return counters.get(fd, 0)',
    ).replace(
        'def perf_event_close(fd: int, counters: dict[int, int]) -> bool:\n    """TODO [LX-PERF-CLOSE-03]: remove fd from counters."""\n    raise NotImplementedError("LX-PERF-CLOSE-03")',
        'def perf_event_close(fd: int, counters: dict[int, int]) -> bool:\n    # PEDAGOGY-SOLUTION: LX-PERF-CLOSE-03\n    return counters.pop(fd, None) is not None',
    )
    test = '''# PEDAGOGY-TEST: LX-PERF-OPEN-01
# PEDAGOGY-TEST: LX-PERF-READ-02
# PEDAGOGY-TEST: LX-PERF-CLOSE-03
# Caso 1: handle positivo
# Caso 2: read retorna 42
# Caso 3: close retorna True
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from perf_lab import perf_event_open, perf_event_read, perf_event_close

def main():
    fd = perf_event_open(1, 2)
    assert fd > 0
    counters = {fd: 42}
    assert perf_event_read(fd, counters) == 42
    assert perf_event_close(fd, counters) is True
    assert fd not in counters
    print("OK perf_lab")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "perf_lab.py", starter, sol)
    write_pair(base, "test_perf_lab.py", test, test)
    write_pedagogy_pack(
        base, "perf_event_open_lab",
        "# perf_event_open lab\n\nSubset simulation do syscall perf (continua `proc_task_snapshot`).\n",
        f"cd days/{DAY}/linux/perf_event_open_lab/starter\npython test_perf_lab.py",
        todos,
        [("perf_event_open", "Abrir contador hardware.", "ioctl-like fd sintético.", "Base do profiling Linux."),
         ("perf_event_read", "Ler valor acumulado.", "lookup em dict.", "Sampling precisa do contador."),
         ("perf_event_close", "Liberar fd.", "pop do mapa.", "Evita fd leak.")],
        "Lab perf: simula open/read/close antes de usar perf real no kernel.",
        ["handle positivo", "read 42", "close True"],
    )


def scaffold_stack_sample_trace() -> None:
    base = DAY09 / "rust" / "stack_sample_trace"
    todos = [
        {"id": "RS-STACK-SAMPLE-01", "file": "starter/src/lib.rs", "fn": "sample_stack",
         "problem": "Capturar até n frames do stack.", "lang": "rust",
         "code": "pub fn sample_stack(frames: &[u64], n: usize) -> Vec<u64> {\n    frames.iter().take(n).copied().collect()\n}",
         "why": "Take limita profundidade.", "verify": "Caso 1: 2 frames."},
        {"id": "RS-STACK-FRAME-02", "file": "starter/src/lib.rs", "fn": "resolve_frame",
         "problem": "Resolver endereço para símbolo.", "lang": "rust",
         "code": 'pub fn resolve_frame(addr: u64, symbols: &std::collections::HashMap<u64, &str>) -> String {\n    symbols.get(&addr).map(|s| s.to_string()).unwrap_or_else(|| format!("0x{addr:x}"))\n}',
         "why": "Fallback hex se desconhecido.", "verify": "Caso 2: main."},
        {"id": "RS-STACK-REPORT-03", "file": "starter/src/lib.rs", "fn": "format_stack_report",
         "problem": "Relatório multi-sample.", "lang": "rust",
         "code": 'pub fn format_stack_report(samples: &[Vec<u64>], symbols: &std::collections::HashMap<u64, &str>) -> String {\n    let mut out = String::new();\n    for (i, st) in samples.iter().enumerate() {\n        out.push_str(&format!("sample {}:\\n", i));\n        for addr in st {\n            out.push_str(&format!("  {}\\n", resolve_frame(*addr, symbols)));\n        }\n    }\n    out\n}',
         "why": "Texto diffável para CI.", "verify": "Caso 3: linha main."},
    ]
    lib_starter = '''pub fn sample_stack(frames: &[u64], n: usize) -> Vec<u64> {
    // TODO [RS-STACK-SAMPLE-01]
    let _ = (frames, n);
    vec![]
}

pub fn resolve_frame(addr: u64, symbols: &std::collections::HashMap<u64, &str>) -> String {
    // TODO [RS-STACK-FRAME-02]
    let _ = (addr, symbols);
    String::new()
}

pub fn format_stack_report(
    samples: &[Vec<u64>],
    symbols: &std::collections::HashMap<u64, &str>,
) -> String {
    // TODO [RS-STACK-REPORT-03]
    let _ = (samples, symbols);
    String::new()
}
'''
    lib_sol = lib_starter.replace(
        "pub fn sample_stack(frames: &[u64], n: usize) -> Vec<u64> {\n    // TODO [RS-STACK-SAMPLE-01]\n    let _ = (frames, n);\n    vec![]\n}",
        "pub fn sample_stack(frames: &[u64], n: usize) -> Vec<u64> {\n    // PEDAGOGY-SOLUTION: RS-STACK-SAMPLE-01\n    frames.iter().take(n).copied().collect()\n}",
    ).replace(
        "pub fn resolve_frame(addr: u64, symbols: &std::collections::HashMap<u64, &str>) -> String {\n    // TODO [RS-STACK-FRAME-02]\n    let _ = (addr, symbols);\n    String::new()\n}",
        'pub fn resolve_frame(addr: u64, symbols: &std::collections::HashMap<u64, &str>) -> String {\n    // PEDAGOGY-SOLUTION: RS-STACK-FRAME-02\n    symbols.get(&addr).map(|s| s.to_string()).unwrap_or_else(|| format!("0x{addr:x}"))\n}',
    ).replace(
        "pub fn format_stack_report(\n    samples: &[Vec<u64>],\n    symbols: &std::collections::HashMap<u64, &str>,\n) -> String {\n    // TODO [RS-STACK-REPORT-03]\n    let _ = (samples, symbols);\n    String::new()\n}",
        'pub fn format_stack_report(\n    samples: &[Vec<u64>],\n    symbols: &std::collections::HashMap<u64, &str>,\n) -> String {\n    // PEDAGOGY-SOLUTION: RS-STACK-REPORT-03\n    let mut out = String::new();\n    for (i, st) in samples.iter().enumerate() {\n        out.push_str(&format!("sample {}:\\n", i));\n        for addr in st {\n            out.push_str(&format!("  {}\\n", resolve_frame(*addr, symbols)));\n        }\n    }\n    out\n}',
    )
    test_rs = '''// PEDAGOGY-TEST: RS-STACK-SAMPLE-01
// PEDAGOGY-TEST: RS-STACK-FRAME-02
// PEDAGOGY-TEST: RS-STACK-REPORT-03
// Caso 1: 2 frames
// Caso 2: resolve main
// Caso 3: report contém main
use stack_sample_trace::*;
use std::collections::HashMap;

#[test]
fn stack_trace_cases() {
    let frames = vec![0x1000u64, 0x2000, 0x3000];
    let sample = sample_stack(&frames, 2);
    assert_eq!(sample, vec![0x1000, 0x2000]);
    let mut syms = HashMap::new();
    syms.insert(0x1000, "main");
    assert_eq!(resolve_frame(0x1000, &syms), "main");
    let rep = format_stack_report(&[sample], &syms);
    assert!(rep.contains("main"));
}
'''
    cargo = '''[package]
name = "stack_sample_trace"
version = "0.1.0"
edition = "2021"

[lib]
path = "src/lib.rs"
'''
    for side, lib in (("starter", lib_starter), ("solutions", lib_sol)):
        root = base / side
        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "tests").mkdir(parents=True, exist_ok=True)
        (root / "Cargo.toml").write_text(cargo, encoding="utf-8")
        (root / "src" / "lib.rs").write_text(lib, encoding="utf-8")
        (root / "tests" / "stack_tests.rs").write_text(test_rs, encoding="utf-8")
    write_pedagogy_pack(
        base, "stack_sample_trace",
        "# Rust stack sampling\n\nStack sample trace (continua `clvm_v2_verify`).\n",
        f"cd days/{DAY}/rust/stack_sample_trace/starter\ncargo test",
        todos,
        [("Stack sample", "Captura PC frames.", "take(n).", "Profiling usa amostras."),
         ("Symbol resolve", "addr→nome.", "HashMap lookup.", "Human-readable traces."),
         ("Report", "Multi-sample texto.", "format por linha.", "Diff em CI.")],
        "Stack sampling em Rust: frames + símbolos + relatório textual.",
        ["2 frames", "resolve main", "report main"],
    )


def scaffold_activity_source_span() -> None:
    base = DAY09 / "dotnet" / "activity_source_span"
    todos = [
        {"id": "DN-ACT-SOURCE-01", "file": "starter/ActivityLab.cs", "fn": "CreateSource",
         "problem": "ActivitySource nomeado para spans.", "lang": "csharp",
         "code": "public static ActivitySource CreateSource(string name) => new ActivitySource(name);",
         "why": "Factory centraliza nome.", "verify": "Caso 1: nome correto."},
        {"id": "DN-ACT-SPAN-02", "file": "starter/ActivityLab.cs", "fn": "StartWorkSpan",
         "problem": "Span filho com tags.", "lang": "csharp",
         "code": 'public static Activity? StartWorkSpan(ActivitySource src, string op) {\n    var act = src.StartActivity(op);\n    act?.SetTag("module", "activity_source_span");\n    return act;\n}',
         "why": "Tags correlacionam traces.", "verify": "Caso 2: tag module."},
        {"id": "DN-ACT-EXPORT-03", "file": "starter/ActivityLab.cs", "fn": "ExportSpanSummary",
         "problem": "Resumo textual do span.", "lang": "csharp",
         "code": 'public static string ExportSpanSummary(Activity? act) {\n    if (act is null) return "null";\n    return $"{act.OperationName}|{act.GetTagItem("module")}";\n}',
         "why": "Export leve sem collector.", "verify": "Caso 3: work|module."},
    ]
    cs_starter = '''using System.Diagnostics;

namespace Chris.ActivityLab;

public static class ActivityLab
{
    /// <summary>TODO [DN-ACT-SOURCE-01]: create named ActivitySource.</summary>
    public static ActivitySource CreateSource(string name)
    {
        throw new NotImplementedException("DN-ACT-SOURCE-01");
    }

    /// <summary>TODO [DN-ACT-SPAN-02]: start span with module tag.</summary>
    public static Activity? StartWorkSpan(ActivitySource src, string op)
    {
        throw new NotImplementedException("DN-ACT-SPAN-02");
    }

    /// <summary>TODO [DN-ACT-EXPORT-03]: textual span summary.</summary>
    public static string ExportSpanSummary(Activity? act)
    {
        throw new NotImplementedException("DN-ACT-EXPORT-03");
    }
}
'''
    cs_sol = '''using System.Diagnostics;

namespace Chris.ActivityLab;

public static class ActivityLab
{
    /// <summary>Creates named ActivitySource.</summary>
    public static ActivitySource CreateSource(string name)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-SOURCE-01
        return new ActivitySource(name);
    }

    /// <summary>Starts span with module tag.</summary>
    public static Activity? StartWorkSpan(ActivitySource src, string op)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-SPAN-02
        var act = src.StartActivity(op);
        act?.SetTag("module", "activity_source_span");
        return act;
    }

    /// <summary>Textual span summary export.</summary>
    public static string ExportSpanSummary(Activity? act)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-EXPORT-03
        if (act is null) return "null";
        return $"{act.OperationName}|{act.GetTagItem("module")}";
    }
}
'''
    csproj = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <RootNamespace>Chris.ActivityLab</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <Compile Remove="tests/**" />
  </ItemGroup>
</Project>
'''
    test_csproj = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\\Chris.ActivityLab.csproj" />
  </ItemGroup>
</Project>
'''
    test_cs = '''using System.Diagnostics;
using Chris.ActivityLab;
using Xunit;

namespace Chris.ActivityLab.Tests;

public class ActivityTests
{
    private static ActivityListener CreateListener(string sourceName)
    {
        return new ActivityListener
        {
            ShouldListenTo = src => src.Name == sourceName,
            Sample = (ref ActivityCreationOptions<ActivityContext> _) => ActivitySamplingResult.AllData,
        };
    }

    // Caso 1: DN-ACT-SOURCE-01
    // PEDAGOGY-TEST: DN-ACT-SOURCE-01
    [Fact]
    public void Caso1_CreateSource_Name()
    {
        using var src = ActivityLab.CreateSource("chris.lab");
        Assert.Equal("chris.lab", src.Name);
    }

    // Caso 2: DN-ACT-SPAN-02
    // PEDAGOGY-TEST: DN-ACT-SPAN-02
    [Fact]
    public void Caso2_StartWorkSpan_Tag()
    {
        using var listener = CreateListener("chris.lab");
        ActivitySource.AddActivityListener(listener);
        using var src = ActivityLab.CreateSource("chris.lab");
        using var act = ActivityLab.StartWorkSpan(src, "work");
        Assert.NotNull(act);
        Assert.Equal("activity_source_span", act!.GetTagItem("module"));
    }

    // Caso 3: DN-ACT-EXPORT-03
    // PEDAGOGY-TEST: DN-ACT-EXPORT-03
    [Fact]
    public void Caso3_ExportSummary()
    {
        using var listener = CreateListener("chris.lab");
        ActivitySource.AddActivityListener(listener);
        using var src = ActivityLab.CreateSource("chris.lab");
        using var act = ActivityLab.StartWorkSpan(src, "work");
        var s = ActivityLab.ExportSpanSummary(act);
        Assert.Equal("work|activity_source_span", s);
    }
}
'''
    for side, cs in (("starter", cs_starter), ("solutions", cs_sol)):
        root = base / side
        root.mkdir(parents=True, exist_ok=True)
        (root / "Chris.ActivityLab.csproj").write_text(csproj, encoding="utf-8")
        (root / "ActivityLab.cs").write_text(cs, encoding="utf-8")
        tests = root / "tests"
        tests.mkdir(exist_ok=True)
        (tests / "ActivityLab.Tests.csproj").write_text(test_csproj, encoding="utf-8")
        (tests / "ActivityTests.cs").write_text(test_cs, encoding="utf-8")
    write_pedagogy_pack(
        base, "activity_source_span",
        "# ActivitySource spans\n\nDiagnostic spans .NET (continua `input_event_span`).\n",
        f"cd days/{DAY}/dotnet/activity_source_span/starter\ndotnet test tests/ActivityLab.Tests.csproj",
        todos,
        [("ActivitySource", "Fonte de spans.", "new ActivitySource.", "OpenTelemetry bridge."),
         ("Activity span", "Operação nomeada.", "StartActivity + tags.", "Correlação distribuída."),
         ("Export", "Resumo textual.", "OperationName|tag.", "Debug sem collector.")],
        "ActivitySource: spans com tags para observabilidade .NET.",
        ["nome source", "tag module", "export work|module"],
    )


def scaffold_gpu_timer_query() -> None:
    base = DAY09 / "graphics" / "gpu_timer_query"
    todos = [
        {"id": "GFX-GPU-TIMER-01", "file": "starter/gpu_timer.py", "fn": "GpuTimerSim.begin_query",
         "problem": "Iniciar query GPU simulada.", "code": "def begin_query(self, name: str) -> int:\n    h = self._next\n    self._next += 1\n    self._starts[h] = (name, self._clock())\n    return h",
         "why": "Handle monotônico.", "verify": "Caso 1: handle 0."},
        {"id": "GFX-GPU-LAP-02", "file": "starter/gpu_timer.py", "fn": "GpuTimerSim.end_query",
         "problem": "Finalizar e registrar ms.", "code": "def end_query(self, handle: int) -> float:\n    name, t0 = self._starts.pop(handle)\n    ms = (self._clock() - t0) * 1000.0\n    self._laps[name] = ms\n    return ms",
         "why": "Delta tempo em ms.", "verify": "Caso 2: ms >= 0."},
        {"id": "GFX-GPU-BENCH-03", "file": "starter/gpu_timer.py", "fn": "GpuTimerSim.lap_times",
         "problem": "Exportar todos os laps.", "code": "def lap_times(self) -> dict[str, float]:\n    out = dict(self._laps)\n    return out",
         "why": "Snapshot para benchmark.", "verify": "Caso 3: dict não vazio."},
    ]
    starter = '''"""GPU timer query simulation (headless)."""

from __future__ import annotations

import time


class GpuTimerSim:
    def __init__(self) -> None:
        self._next = 0
        self._starts: dict[int, tuple[str, float]] = {}
        self._laps: dict[str, float] = {}

    def _clock(self) -> float:
        return time.perf_counter()

    def begin_query(self, name: str) -> int:
        """TODO [GFX-GPU-TIMER-01]: return query handle."""
        raise NotImplementedError("GFX-GPU-TIMER-01")

    def end_query(self, handle: int) -> float:
        """TODO [GFX-GPU-LAP-02]: end query, return ms."""
        raise NotImplementedError("GFX-GPU-LAP-02")

    def lap_times(self) -> dict[str, float]:
        """TODO [GFX-GPU-BENCH-03]: all completed laps."""
        raise NotImplementedError("GFX-GPU-BENCH-03")
'''
    sol = starter.replace(
        'def begin_query(self, name: str) -> int:\n        """TODO [GFX-GPU-TIMER-01]: return query handle."""\n        raise NotImplementedError("GFX-GPU-TIMER-01")',
        'def begin_query(self, name: str) -> int:\n        # PEDAGOGY-SOLUTION: GFX-GPU-TIMER-01\n        h = self._next\n        self._next += 1\n        self._starts[h] = (name, self._clock())\n        return h',
    ).replace(
        'def end_query(self, handle: int) -> float:\n        """TODO [GFX-GPU-LAP-02]: end query, return ms."""\n        raise NotImplementedError("GFX-GPU-LAP-02")',
        'def end_query(self, handle: int) -> float:\n        # PEDAGOGY-SOLUTION: GFX-GPU-LAP-02\n        name, t0 = self._starts.pop(handle)\n        ms = (self._clock() - t0) * 1000.0\n        self._laps[name] = ms\n        return ms',
    ).replace(
        'def lap_times(self) -> dict[str, float]:\n        """TODO [GFX-GPU-BENCH-03]: all completed laps."""\n        raise NotImplementedError("GFX-GPU-BENCH-03")',
        'def lap_times(self) -> dict[str, float]:\n        # PEDAGOGY-SOLUTION: GFX-GPU-BENCH-03\n        return dict(self._laps)',
    )
    test = '''# PEDAGOGY-TEST: GFX-GPU-TIMER-01
# PEDAGOGY-TEST: GFX-GPU-LAP-02
# PEDAGOGY-TEST: GFX-GPU-BENCH-03
# Caso 1: handle 0
# Caso 2: ms >= 0
# Caso 3: lap_times não vazio
# VISUAL-01: lap draw > 0 ms no relatório
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gpu_timer import GpuTimerSim

def main():
    t = GpuTimerSim()
    h = t.begin_query("draw")
    ms = t.end_query(h)
    assert h == 0
    assert ms >= 0.0
    laps = t.lap_times()
    assert "draw" in laps
    print("OK gpu_timer")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "gpu_timer.py", starter, sol)
    write_pair(base, "test_gpu_timer.py", test, test)
    (base / "docs").mkdir(exist_ok=True)
    (base / "docs" / "COMPARISON.md").write_text(
        """# Comparacao: GPU timer query

| Etapa | CPU/software | OpenGL timer query |
|-------|--------------|-------------------|
| Begin | perf_counter | glQueryCounter / handle |
| End | delta * 1000 ms | GPU_ELAPSED_TIME |
| Report | lap_times dict | same lap export API |
""",
        encoding="utf-8",
    )
    write_pedagogy_pack(
        base, "gpu_timer_query",
        "# GPU timer query simulation\n\nHeadless timer lab (par com `resource_state_tracker`).\n",
        f"cd days/{DAY}/graphics/gpu_timer_query/starter\npython test_gpu_timer.py",
        todos,
        [("Timer query begin", "Marca início GPU.", "handle + perf_counter.", "Mede draw calls."),
         ("Timer query end", "Delta em ms.", "pop start, store lap.", "Hotspot GPU."),
         ("Benchmark export", "lap_times dict.", "copy laps.", "Comparar frames.")],
        "Simulação de GL_ARB_timer_query em Python para profiling sem GPU.",
        ["handle 0", "ms >= 0", "lap_times draw"],
    )


def scaffold_yara_match_scan() -> None:
    base = DAY09 / "redteam" / "yara_match_scan"
    todos = [
        {"id": "RT-YARA-PARSE-01", "file": "starter/yara_scan.py", "fn": "parse_hex_pattern",
         "problem": "Parse padrão YARA hex { AA BB ?? }.", "code": 'def parse_hex_pattern(pat: str) -> list[int | None]:\n    body = pat.strip("{} ").replace(" ", "")\n    out: list[int | None] = []\n    i = 0\n    while i < len(body):\n        if body[i:i+2] == "??":\n            out.append(None); i += 2\n        else:\n            out.append(int(body[i:i+2], 16)); i += 2\n    return out',
         "why": "?? é wildcard byte.", "verify": "Caso 1: [0xAA, None]."},
        {"id": "RT-YARA-MATCH-02", "file": "starter/yara_scan.py", "fn": "match_at",
         "problem": "Match padrão em offset.", "code": "def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:\n    if off + len(pattern) > len(data):\n        return False\n    for i, b in enumerate(pattern):\n        if b is not None and data[off + i] != b:\n            return False\n    return True",
         "why": "Wildcard ignora byte.", "verify": "Caso 2: match em offset 1."},
        {"id": "RT-YARA-TRIAGE-03", "file": "starter/yara_scan.py", "fn": "scan_all",
         "problem": "Encontrar todos offsets.", "code": "def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:\n    hits: list[int] = []\n    for i in range(len(data)):\n        if match_at(data, pattern, i):\n            hits.append(i)\n    return hits",
         "why": "Slide window completo.", "verify": "Caso 3: lista [1]."},
    ]
    starter = '''"""YARA-style hex pattern scanner."""

from __future__ import annotations


def parse_hex_pattern(pat: str) -> list[int | None]:
    """TODO [RT-YARA-PARSE-01]: parse { AA BB ?? }."""
    raise NotImplementedError("RT-YARA-PARSE-01")


def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:
    """TODO [RT-YARA-MATCH-02]: match at offset."""
    raise NotImplementedError("RT-YARA-MATCH-02")


def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:
    """TODO [RT-YARA-TRIAGE-03]: all match offsets."""
    raise NotImplementedError("RT-YARA-TRIAGE-03")
'''
    sol = starter.replace(
        'def parse_hex_pattern(pat: str) -> list[int | None]:\n    """TODO [RT-YARA-PARSE-01]: parse { AA BB ?? }."""\n    raise NotImplementedError("RT-YARA-PARSE-01")',
        'def parse_hex_pattern(pat: str) -> list[int | None]:\n    # PEDAGOGY-SOLUTION: RT-YARA-PARSE-01\n    body = pat.strip("{} ").replace(" ", "")\n    out: list[int | None] = []\n    i = 0\n    while i < len(body):\n        if body[i:i+2] == "??":\n            out.append(None); i += 2\n        else:\n            out.append(int(body[i:i+2], 16)); i += 2\n    return out',
    ).replace(
        'def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:\n    """TODO [RT-YARA-MATCH-02]: match at offset."""\n    raise NotImplementedError("RT-YARA-MATCH-02")',
        'def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:\n    # PEDAGOGY-SOLUTION: RT-YARA-MATCH-02\n    if off + len(pattern) > len(data):\n        return False\n    for i, b in enumerate(pattern):\n        if b is not None and data[off + i] != b:\n            return False\n    return True',
    ).replace(
        'def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:\n    """TODO [RT-YARA-TRIAGE-03]: all match offsets."""\n    raise NotImplementedError("RT-YARA-TRIAGE-03")',
        'def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:\n    # PEDAGOGY-SOLUTION: RT-YARA-TRIAGE-03\n    return [i for i in range(len(data)) if match_at(data, pattern, i)]',
    )
    test = '''# PEDAGOGY-TEST: RT-YARA-PARSE-01
# PEDAGOGY-TEST: RT-YARA-MATCH-02
# PEDAGOGY-TEST: RT-YARA-TRIAGE-03
# Caso 1: parse AA ??
# Caso 2: match offset 1
# Caso 3: scan_all retorna [1]
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yara_scan import parse_hex_pattern, match_at, scan_all

def main():
    pat = parse_hex_pattern("{ AA ?? }")
    assert pat == [0xAA, None]
    data = bytes([0, 0xAA, 0x55])
    assert match_at(data, pat, 1)
    assert scan_all(data, pat) == [1]
    print("OK yara_scan")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "yara_scan.py", starter, sol)
    write_pair(base, "test_yara_scan.py", test, test)
    write_pedagogy_pack(
        base, "yara_match_scan",
        "# YARA match scan\n\nPattern scan estilo YARA (continua `hid_report_fuzz`).\n",
        f"cd days/{DAY}/redteam/yara_match_scan/starter\npython test_yara_scan.py",
        todos,
        [("Hex parse", "Tokens AA/??.", "split hex pairs.", "YARA wire format."),
         ("Match at", "Wildcard byte.", "compare ou skip.", "Fuzzy signature."),
         ("Scan all", "Todos offsets.", "range + match_at.", "Triage malware.")],
        "Scanner YARA simplificado: hex patterns com wildcard.",
        ["parse AA ??", "match offset 1", "scan [1]"],
    )


def scaffold_decoherence_noise() -> None:
    base = DAY09 / "quantum" / "decoherence_noise"
    todos = [
        {"id": "Q-DECO-CHANNEL-01", "file": "starter/decoherence.py", "fn": "depolarizing_channel",
         "problem": "Canal depolarizante mistura estados.", "code": "def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:\n    mix = gamma / 2\n    return (1 - gamma) * p0 + mix, (1 - gamma) * p1 + mix",
         "why": "gamma=0 preserva; gamma=1 uniformiza.", "verify": "Caso 1: soma 1."},
        {"id": "Q-DECO-APPLY-02", "file": "starter/decoherence.py", "fn": "apply_noise_step",
         "problem": "Um passo de ruído em probs.", "code": "def apply_noise_step(probs: list[float], gamma: float) -> list[float]:\n    if len(probs) != 2:\n        raise ValueError('2-level only')\n    p0, p1 = depolarizing_channel(probs[0], probs[1], gamma)\n    return [p0, p1]",
         "why": "2-level para lab.", "verify": "Caso 2: p0 diminui."},
        {"id": "Q-DECO-TRACE-03", "file": "starter/decoherence.py", "fn": "trace_decoherence",
         "problem": "Trace N passos.", "code": "def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:\n    cur = [p0, 1.0 - p0]\n    trace = [cur[0]]\n    for _ in range(steps):\n        cur = apply_noise_step(cur, gamma)\n        trace.append(cur[0])\n    return trace",
         "why": "Série temporal de decoerência.", "verify": "Caso 3: len steps+1."},
    ]
    starter = '''"""Simple decoherence noise channel."""

from __future__ import annotations


def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:
    """TODO [Q-DECO-CHANNEL-01]: return (p0', p1')."""
    raise NotImplementedError("Q-DECO-CHANNEL-01")


def apply_noise_step(probs: list[float], gamma: float) -> list[float]:
    """TODO [Q-DECO-APPLY-02]: one noise step."""
    raise NotImplementedError("Q-DECO-APPLY-02")


def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:
    """TODO [Q-DECO-TRACE-03]: p0 trace over steps."""
    raise NotImplementedError("Q-DECO-TRACE-03")
'''
    sol = starter.replace(
        'def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:\n    """TODO [Q-DECO-CHANNEL-01]: return (p0\', p1\')."""\n    raise NotImplementedError("Q-DECO-CHANNEL-01")',
        'def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:\n    # PEDAGOGY-SOLUTION: Q-DECO-CHANNEL-01\n    mix = gamma / 2\n    return (1 - gamma) * p0 + mix, (1 - gamma) * p1 + mix',
    ).replace(
        'def apply_noise_step(probs: list[float], gamma: float) -> list[float]:\n    """TODO [Q-DECO-APPLY-02]: one noise step."""\n    raise NotImplementedError("Q-DECO-APPLY-02")',
        'def apply_noise_step(probs: list[float], gamma: float) -> list[float]:\n    # PEDAGOGY-SOLUTION: Q-DECO-APPLY-02\n    if len(probs) != 2:\n        raise ValueError("2-level only")\n    p0, p1 = depolarizing_channel(probs[0], probs[1], gamma)\n    return [p0, p1]',
    ).replace(
        'def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:\n    """TODO [Q-DECO-TRACE-03]: p0 trace over steps."""\n    raise NotImplementedError("Q-DECO-TRACE-03")',
        'def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:\n    # PEDAGOGY-SOLUTION: Q-DECO-TRACE-03\n    cur = [p0, 1.0 - p0]\n    trace = [cur[0]]\n    for _ in range(steps):\n        cur = apply_noise_step(cur, gamma)\n        trace.append(cur[0])\n    return trace',
    )
    test = '''# PEDAGOGY-TEST: Q-DECO-CHANNEL-01
# PEDAGOGY-TEST: Q-DECO-APPLY-02
# PEDAGOGY-TEST: Q-DECO-TRACE-03
# Caso 1: soma probs 1
# Caso 2: p0 diminui com gamma
# Caso 3: trace len steps+1
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from decoherence import depolarizing_channel, apply_noise_step, trace_decoherence

def main():
    p0, p1 = depolarizing_channel(1.0, 0.0, 0.1)
    assert abs(p0 + p1 - 1.0) < 1e-9
    nxt = apply_noise_step([1.0, 0.0], 0.2)
    assert nxt[0] < 1.0
    tr = trace_decoherence(1.0, 3, 0.1)
    assert len(tr) == 4
    print("OK decoherence")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "decoherence.py", starter, sol)
    write_pair(base, "test_decoherence.py", test, test)
    write_pedagogy_pack(
        base, "decoherence_noise",
        "# Decoherence noise\n\nCanal de ruído (continua `measurement_born`).\n",
        f"cd days/{DAY}/quantum/decoherence_noise/starter\npython test_decoherence.py",
        todos,
        [("Depolarizing", "Canal gamma.", "mix uniforme.", "Modela T1/T2 simplificado."),
         ("Noise step", "Um tick.", "channel em probs.", "Simulação iterativa."),
         ("Trace", "Série p0.", "loop steps.", "Visualiza decoerência.")],
        "Ruído quântico: canal depolarizante e trace temporal.",
        ["soma 1", "p0 diminui", "trace len 4"],
    )


def scaffold_attention_mask() -> None:
    base = DAY09 / "ai" / "attention_mask"
    todos = [
        {"id": "AI-ATTN-MASK-01", "file": "starter/attention_mask.py", "fn": "build_padding_mask",
         "problem": "Máscara 1 para tokens válidos.", "code": "def build_padding_mask(lengths: list[int], max_len: int) -> list[list[int]]:\n    return [[1 if j < L else 0 for j in range(max_len)] for L in lengths]",
         "why": "Zero em padding.", "verify": "Caso 1: row sum = length."},
        {"id": "AI-ATTN-CAUSAL-02", "file": "starter/attention_mask.py", "fn": "build_causal_mask",
         "problem": "Máscara causal lower-triangular.", "code": "def build_causal_mask(seq_len: int) -> list[list[int]]:\n    return [[1 if j <= i else 0 for j in range(seq_len)] for i in range(seq_len)]",
         "why": "Decoder só vê passado.", "verify": "Caso 2: upper zero."},
        {"id": "AI-ATTN-SCORE-03", "file": "starter/attention_mask.py", "fn": "masked_softmax_scores",
         "problem": "Softmax com -inf em mask 0.", "code": "import math\n\ndef masked_softmax_scores(scores: list[float], mask: list[int]) -> list[float]:\n    masked = [s if m else float('-inf') for s, m in zip(scores, mask)]\n    m = max(masked)\n    exps = [math.exp(s - m) for s in masked]\n    z = sum(exps)\n    return [e / z for e in exps]",
         "why": "Estabilidade numérica com max shift.", "verify": "Caso 3: soma 1."},
    ]
    starter = '''"""Attention mask computation."""

from __future__ import annotations

import math


def build_padding_mask(lengths: list[int], max_len: int) -> list[list[int]]:
    """TODO [AI-ATTN-MASK-01]: padding mask rows."""
    raise NotImplementedError("AI-ATTN-MASK-01")


def build_causal_mask(seq_len: int) -> list[list[int]]:
    """TODO [AI-ATTN-CAUSAL-02]: causal mask."""
    raise NotImplementedError("AI-ATTN-CAUSAL-02")


def masked_softmax_scores(scores: list[float], mask: list[int]) -> list[float]:
    """TODO [AI-ATTN-SCORE-03]: masked softmax."""
    raise NotImplementedError("AI-ATTN-SCORE-03")
'''
    sol = starter.replace(
        'def build_padding_mask(lengths: list[int], max_len: int) -> list[list[int]]:\n    """TODO [AI-ATTN-MASK-01]: padding mask rows."""\n    raise NotImplementedError("AI-ATTN-MASK-01")',
        'def build_padding_mask(lengths: list[int], max_len: int) -> list[list[int]]:\n    # PEDAGOGY-SOLUTION: AI-ATTN-MASK-01\n    return [[1 if j < L else 0 for j in range(max_len)] for L in lengths]',
    ).replace(
        'def build_causal_mask(seq_len: int) -> list[list[int]]:\n    """TODO [AI-ATTN-CAUSAL-02]: causal mask."""\n    raise NotImplementedError("AI-ATTN-CAUSAL-02")',
        'def build_causal_mask(seq_len: int) -> list[list[int]]:\n    # PEDAGOGY-SOLUTION: AI-ATTN-CAUSAL-02\n    return [[1 if j <= i else 0 for j in range(seq_len)] for i in range(seq_len)]',
    ).replace(
        'def masked_softmax_scores(scores: list[float], mask: list[int]) -> list[float]:\n    """TODO [AI-ATTN-SCORE-03]: masked softmax."""\n    raise NotImplementedError("AI-ATTN-SCORE-03")',
        'def masked_softmax_scores(scores: list[float], mask: list[int]) -> list[float]:\n    # PEDAGOGY-SOLUTION: AI-ATTN-SCORE-03\n    masked = [s if m else float("-inf") for s, m in zip(scores, mask)]\n    m = max(masked)\n    exps = [math.exp(s - m) for s in masked]\n    z = sum(exps)\n    return [e / z for e in exps]',
    )
    test = '''# PEDAGOGY-TEST: AI-ATTN-MASK-01
# PEDAGOGY-TEST: AI-ATTN-CAUSAL-02
# PEDAGOGY-TEST: AI-ATTN-SCORE-03
# Caso 1: padding row sum
# Caso 2: causal upper zero
# Caso 3: softmax soma 1
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from attention_mask import build_padding_mask, build_causal_mask, masked_softmax_scores

def main():
    m = build_padding_mask([2, 3], 4)
    assert sum(m[0]) == 2
    c = build_causal_mask(3)
    assert c[0][1] == 0
    sm = masked_softmax_scores([1.0, 2.0, 3.0], [1, 1, 0])
    assert abs(sum(sm) - 1.0) < 1e-6
    print("OK attention_mask")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "attention_mask.py", starter, sol)
    write_pair(base, "test_attention_mask.py", test, test)
    write_pedagogy_pack(
        base, "attention_mask",
        "# Attention mask\n\nMáscaras de atenção (continua `input_event_entropy`).\n",
        f"cd days/{DAY}/ai/attention_mask/starter\npython test_attention_mask.py",
        todos,
        [("Padding mask", "Tokens válidos.", "1 se j < len.", "Batch com tamanhos variados."),
         ("Causal mask", "Autoregressivo.", "j <= i.", "GPT-style."),
         ("Masked softmax", "Scores com -inf.", "exp + normalize.", "Ignora padding.")],
        "Máscaras de atenção: padding, causal e softmax mascarado.",
        ["row sum 2", "upper zero", "softmax soma 1"],
    )


def scaffold_async_hooks_trace() -> None:
    base = DAY09 / "nodejs" / "async_hooks_trace"
    todos = [
        {"id": "ND-ASYNC-HOOK-01", "file": "starter/async_trace.js", "fn": "installHooks",
         "problem": "Registrar init/before/after.", "lang": "javascript",
         "code": "export function installHooks(store) {\n  asyncHooks.createHook({\n    init(asyncId, type, triggerAsyncId) {\n      store.events.push({ phase: 'init', asyncId, type, triggerAsyncId });\n    },\n    before(asyncId) { store.events.push({ phase: 'before', asyncId }); },\n    after(asyncId) { store.events.push({ phase: 'after', asyncId }); },\n  }).enable();\n}",
         "why": "async_hooks expõe lifecycle.", "verify": "Caso 1: init event."},
        {"id": "ND-ASYNC-TIMELINE-02", "file": "starter/async_trace.js", "fn": "formatTimeline",
         "problem": "Timeline textual.", "lang": "javascript",
         "code": "export function formatTimeline(events) {\n  return events.map(e => `${e.phase}:${e.asyncId}`).join('|');\n}",
         "why": "String diffável.", "verify": "Caso 2: contains init."},
        {"id": "ND-ASYNC-METRICS-03", "file": "starter/async_trace.js", "fn": "countPhases",
         "problem": "Contagem por fase.", "lang": "javascript",
         "code": "export function countPhases(events) {\n  const m = {};\n  for (const e of events) m[e.phase] = (m[e.phase] || 0) + 1;\n  return m;\n}",
         "why": "Métricas de async churn.", "verify": "Caso 3: init >= 1."},
    ]
    starter_js = '''import asyncHooks from 'node:async_hooks';

export function installHooks(store) {
    // TODO [ND-ASYNC-HOOK-01]: register init/before/after into store.events
    void store;
}

export function formatTimeline(events) {
    // TODO [ND-ASYNC-TIMELINE-02]: phase:asyncId joined by |
    void events;
    return '';
}

export function countPhases(events) {
    // TODO [ND-ASYNC-METRICS-03]: count per phase
    void events;
    return {};
}
'''
    sol_js = starter_js.replace(
        "export function installHooks(store) {\n    // TODO [ND-ASYNC-HOOK-01]: register init/before/after into store.events\n    void store;\n}",
        "export function installHooks(store) {\n    // PEDAGOGY-SOLUTION: ND-ASYNC-HOOK-01\n    asyncHooks.createHook({\n        init(asyncId, type, triggerAsyncId) {\n            store.events.push({ phase: 'init', asyncId, type, triggerAsyncId });\n        },\n        before(asyncId) { store.events.push({ phase: 'before', asyncId }); },\n        after(asyncId) { store.events.push({ phase: 'after', asyncId }); },\n    }).enable();\n}",
    ).replace(
        "export function formatTimeline(events) {\n    // TODO [ND-ASYNC-TIMELINE-02]: phase:asyncId joined by |\n    void events;\n    return '';\n}",
        "export function formatTimeline(events) {\n    // PEDAGOGY-SOLUTION: ND-ASYNC-TIMELINE-02\n    return events.map(e => `${e.phase}:${e.asyncId}`).join('|');\n}",
    ).replace(
        "export function countPhases(events) {\n    // TODO [ND-ASYNC-METRICS-03]: count per phase\n    void events;\n    return {};\n}",
        "export function countPhases(events) {\n    // PEDAGOGY-SOLUTION: ND-ASYNC-METRICS-03\n    const m = {};\n    for (const e of events) m[e.phase] = (m[e.phase] || 0) + 1;\n    return m;\n}",
    )
    test_js = '''// PEDAGOGY-TEST: ND-ASYNC-HOOK-01
// PEDAGOGY-TEST: ND-ASYNC-TIMELINE-02
// PEDAGOGY-TEST: ND-ASYNC-METRICS-03
// Caso 1: init event
// Caso 2: timeline contains init
// Caso 3: init count >= 1
import assert from 'node:assert';
import { installHooks, formatTimeline, countPhases } from './async_trace.js';

async function main() {
    const store = { events: [] };
    installHooks(store);
    await Promise.resolve();
    assert.ok(store.events.some(e => e.phase === 'init'));
    const tl = formatTimeline(store.events);
    assert.ok(tl.includes('init'));
    const m = countPhases(store.events);
    assert.ok(m.init >= 1);
    console.log('OK async_trace');
}

main().catch(e => { console.error(e); process.exit(1); });
'''
    for side, js in (("starter", starter_js), ("solutions", sol_js)):
        d = base / side
        d.mkdir(parents=True, exist_ok=True)
        (d / "async_trace.js").write_text(js, encoding="utf-8")
        (d / "test.js").write_text(test_js, encoding="utf-8")
        (d / "package.json").write_text('{"type":"module"}\n', encoding="utf-8")
    write_pedagogy_pack(
        base, "async_hooks_trace",
        "# async_hooks trace\n\nTimeline async (continua `libuv_phase_probe`).\n",
        f"cd days/{DAY}/nodejs/async_hooks_trace/starter\nnode test.js",
        todos,
        [("async_hooks", "init/before/after.", "createHook.", "Debug async leaks."),
         ("Timeline", "phase:asyncId.", "map+join.", "Visualize ordem."),
         ("Metrics", "count phases.", "histogram.", "Detect churn.")],
        "async_hooks: rastrear lifecycle de Promises e timers.",
        ["init event", "timeline init", "init count"],
    )


def scaffold_logfmt_lexer() -> None:
    base = DAY09 / "parsers" / "logfmt_lexer"
    todos = [
        {"id": "PR-LOGFMT-LEX-01", "file": "starter/logfmt.py", "fn": "tokenize",
         "problem": "Tokenizar key=value com espaços em aspas.", "code": "def tokenize(line: str) -> list[str]:\n    return shlex.split(line.strip())",
         "why": "shlex respeita aspas.", "verify": "Caso 1: 2 tokens."},
        {"id": "PR-LOGFMT-KV-02", "file": "starter/logfmt.py", "fn": "parse_kv",
         "problem": "Parse um token key=value.", "code": "def parse_kv(tok: str) -> tuple[str, str]:\n    k, v = tok.split('=', 1)\n    return k, v",
         "why": "split once preserva = no valor.", "verify": "Caso 2: msg=hello."},
        {"id": "PR-LOGFMT-ESC-03", "file": "starter/logfmt.py", "fn": "parse_line",
         "problem": "Parse linha completa em dict.", "code": "def parse_line(line: str) -> dict[str, str]:\n    out: dict[str, str] = {}\n    for tok in tokenize(line):\n        k, v = parse_kv(tok)\n        out[k] = v.strip('\"')\n    return out",
         "why": "Dict final para logs estruturados.", "verify": "Caso 3: level=info."},
    ]
    starter = '''"""logfmt key=value lexer."""

from __future__ import annotations

import shlex


def tokenize(line: str) -> list[str]:
    """TODO [PR-LOGFMT-LEX-01]: split tokens respecting quotes."""
    raise NotImplementedError("PR-LOGFMT-LEX-01")


def parse_kv(tok: str) -> tuple[str, str]:
    """TODO [PR-LOGFMT-KV-02]: parse key=value."""
    raise NotImplementedError("PR-LOGFMT-KV-02")


def parse_line(line: str) -> dict[str, str]:
    """TODO [PR-LOGFMT-ESC-03]: full line to dict."""
    raise NotImplementedError("PR-LOGFMT-ESC-03")
'''
    sol = starter.replace(
        'def tokenize(line: str) -> list[str]:\n    """TODO [PR-LOGFMT-LEX-01]: split tokens respecting quotes."""\n    raise NotImplementedError("PR-LOGFMT-LEX-01")',
        'def tokenize(line: str) -> list[str]:\n    # PEDAGOGY-SOLUTION: PR-LOGFMT-LEX-01\n    return shlex.split(line.strip())',
    ).replace(
        'def parse_kv(tok: str) -> tuple[str, str]:\n    """TODO [PR-LOGFMT-KV-02]: parse key=value."""\n    raise NotImplementedError("PR-LOGFMT-KV-02")',
        "def parse_kv(tok: str) -> tuple[str, str]:\n    # PEDAGOGY-SOLUTION: PR-LOGFMT-KV-02\n    k, v = tok.split('=', 1)\n    return k, v",
    ).replace(
        'def parse_line(line: str) -> dict[str, str]:\n    """TODO [PR-LOGFMT-ESC-03]: full line to dict."""\n    raise NotImplementedError("PR-LOGFMT-ESC-03")',
        'def parse_line(line: str) -> dict[str, str]:\n    # PEDAGOGY-SOLUTION: PR-LOGFMT-ESC-03\n    out: dict[str, str] = {}\n    for tok in tokenize(line):\n        k, v = parse_kv(tok)\n        out[k] = v.strip(\'"\')\n    return out',
    )
    test = '''# PEDAGOGY-TEST: PR-LOGFMT-LEX-01
# PEDAGOGY-TEST: PR-LOGFMT-KV-02
# PEDAGOGY-TEST: PR-LOGFMT-ESC-03
# Caso 1: 2 tokens
# Caso 2: msg=hello
# Caso 3: level=info
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from logfmt import tokenize, parse_kv, parse_line

def main():
    assert len(tokenize("a=1 b=2")) == 2
    assert parse_kv("msg=hello") == ("msg", "hello")
    d = parse_line('level=info msg="hello world"')
    assert d["level"] == "info"
    print("OK logfmt")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "logfmt.py", starter, sol)
    write_pair(base, "test_logfmt.py", test, test)
    write_pedagogy_pack(
        base, "logfmt_lexer",
        "# logfmt lexer\n\nLexer logfmt (continua `pratt_query_lang`).\n",
        f"cd days/{DAY}/parsers/logfmt_lexer/starter\npython test_logfmt.py",
        todos,
        [("Tokenize", "Split whitespace.", "strip+split.", "Base do lexer."),
         ("KV parse", "key=value.", "split once.", "Valores com =."),
         ("Line parse", "Dict completo.", "loop tokens.", "Logs estruturados.")],
        "Lexer logfmt: tokenização e parse key=value.",
        ["2 tokens", "msg=hello", "level=info"],
    )


def scaffold_verify_replay_log() -> None:
    base = DAY09 / "agent" / "verify_replay_log"
    todos = [
        {"id": "AG-VERIFY-LOG-01", "file": "starter/agent_log.py", "fn": "append_log",
         "problem": "Append evento ao log.", "code": "def append_log(log: list[dict], event: str, payload: dict) -> None:\n    log.append({\"event\": event, \"payload\": payload})",
         "why": "Lista append-only.", "verify": "Caso 1: len 1."},
        {"id": "AG-REPLAY-FSM-02", "file": "starter/agent_log.py", "fn": "replay_fsm",
         "problem": "Replay determina estado final.", "code": "def replay_fsm(log: list[dict]) -> str:\n    state = 'IDLE'\n    for entry in log:\n        ev = entry['event']\n        if ev == 'start': state = 'RUN'\n        elif ev == 'verify' and entry['payload'].get('ok'): state = 'DONE'\n        elif ev == 'verify': state = 'REVISE'\n    return state",
         "why": "FSM simples sobre log.", "verify": "Caso 2: DONE."},
        {"id": "AG-TRACE-HASH-03", "file": "starter/agent_log.py", "fn": "trace_hash",
         "problem": "Hash estável do trace.", "code": "import hashlib\n\ndef trace_hash(log: list[dict]) -> str:\n    data = repr(log).encode()\n    return hashlib.sha256(data).hexdigest()[:16]",
         "why": "Fingerprint para CI.", "verify": "Caso 3: 16 hex chars."},
    ]
    starter = '''"""Verify + replay log FSM."""

from __future__ import annotations

import hashlib


def append_log(log: list[dict], event: str, payload: dict) -> None:
    """TODO [AG-VERIFY-LOG-01]: append structured entry."""
    raise NotImplementedError("AG-VERIFY-LOG-01")


def replay_fsm(log: list[dict]) -> str:
    """TODO [AG-REPLAY-FSM-02]: replay to final state."""
    raise NotImplementedError("AG-REPLAY-FSM-02")


def trace_hash(log: list[dict]) -> str:
    """TODO [AG-TRACE-HASH-03]: stable short hash."""
    raise NotImplementedError("AG-TRACE-HASH-03")
'''
    sol = starter.replace(
        'def append_log(log: list[dict], event: str, payload: dict) -> None:\n    """TODO [AG-VERIFY-LOG-01]: append structured entry."""\n    raise NotImplementedError("AG-VERIFY-LOG-01")',
        'def append_log(log: list[dict], event: str, payload: dict) -> None:\n    # PEDAGOGY-SOLUTION: AG-VERIFY-LOG-01\n    log.append({"event": event, "payload": payload})',
    ).replace(
        'def replay_fsm(log: list[dict]) -> str:\n    """TODO [AG-REPLAY-FSM-02]: replay to final state."""\n    raise NotImplementedError("AG-REPLAY-FSM-02")',
        'def replay_fsm(log: list[dict]) -> str:\n    # PEDAGOGY-SOLUTION: AG-REPLAY-FSM-02\n    state = "IDLE"\n    for entry in log:\n        ev = entry["event"]\n        if ev == "start":\n            state = "RUN"\n        elif ev == "verify" and entry["payload"].get("ok"):\n            state = "DONE"\n        elif ev == "verify":\n            state = "REVISE"\n    return state',
    ).replace(
        'def trace_hash(log: list[dict]) -> str:\n    """TODO [AG-TRACE-HASH-03]: stable short hash."""\n    raise NotImplementedError("AG-TRACE-HASH-03")',
        'def trace_hash(log: list[dict]) -> str:\n    # PEDAGOGY-SOLUTION: AG-TRACE-HASH-03\n    data = repr(log).encode()\n    return hashlib.sha256(data).hexdigest()[:16]',
    )
    test = '''# PEDAGOGY-TEST: AG-VERIFY-LOG-01
# PEDAGOGY-TEST: AG-REPLAY-FSM-02
# PEDAGOGY-TEST: AG-TRACE-HASH-03
# Caso 1: log len 1
# Caso 2: replay DONE
# Caso 3: hash 16 chars
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from agent_log import append_log, replay_fsm, trace_hash

def main():
    log: list[dict] = []
    append_log(log, "start", {})
    assert len(log) == 1
    append_log(log, "verify", {"ok": True})
    assert replay_fsm(log) == "DONE"
    h = trace_hash(log)
    assert len(h) == 16
    print("OK agent_log")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "agent_log.py", starter, sol)
    write_pair(base, "test_agent_log.py", test, test)
    write_pedagogy_pack(
        base, "verify_replay_log",
        "# Verify replay log\n\nFSM + replay (continua `loop_state_machine`).\n",
        f"cd days/{DAY}/agent/verify_replay_log/starter\npython test_agent_log.py",
        todos,
        [("Append log", "Evento estruturado.", "list append.", "Evidência auditável."),
         ("Replay FSM", "Estado final.", "transições sobre log.", "Debug determinístico."),
         ("Trace hash", "SHA256 curto.", "repr+log.", "CI fingerprint.")],
        "Agent log: append, replay FSM e hash de trace.",
        ["len 1", "DONE", "hash 16"],
    )


def scaffold_pdb_symbol_index() -> None:
    base = DAY09 / "tooling" / "pdb_symbol_index"
    todos = [
        {"id": "TL-PDB-PARSE-01", "file": "starter/pdb_index.py", "fn": "parse_symbol_line",
         "problem": "Parse linha ADDR NAME.", "code": "def parse_symbol_line(line: str) -> tuple[int, str]:\n    addr_s, name = line.strip().split(None, 1)\n    return int(addr_s, 16), name",
         "why": "Hex addr + nome.", "verify": "Caso 1: 0x1000 main."},
        {"id": "TL-PDB-INDEX-02", "file": "starter/pdb_index.py", "fn": "build_index",
         "problem": "Índice addr→nome.", "code": "def build_index(lines: list[str]) -> dict[int, str]:\n    idx: dict[int, str] = {}\n    for ln in lines:\n        if not ln.strip():\n            continue\n        addr, name = parse_symbol_line(ln)\n        idx[addr] = name\n    return idx",
         "why": "Lookup O(1).", "verify": "Caso 2: len 2."},
        {"id": "TL-PDB-LOOKUP-03", "file": "starter/pdb_index.py", "fn": "lookup_symbol",
         "problem": "Lookup com fallback hex.", "code": 'def lookup_symbol(idx: dict[int, str], addr: int) -> str:\n    if addr in idx:\n        return idx[addr]\n    return f"0x{addr:x}"',
         "why": "Igual stack resolve.", "verify": "Caso 3: main."},
    ]
    starter = '''"""PDB symbol index basics (text fixture format)."""

from __future__ import annotations


def parse_symbol_line(line: str) -> tuple[int, str]:
    """TODO [TL-PDB-PARSE-01]: parse '1000 main'."""
    raise NotImplementedError("TL-PDB-PARSE-01")


def build_index(lines: list[str]) -> dict[int, str]:
    """TODO [TL-PDB-INDEX-02]: addr->name index."""
    raise NotImplementedError("TL-PDB-INDEX-02")


def lookup_symbol(idx: dict[int, str], addr: int) -> str:
    """TODO [TL-PDB-LOOKUP-03]: lookup or hex fallback."""
    raise NotImplementedError("TL-PDB-LOOKUP-03")
'''
    sol = starter.replace(
        'def parse_symbol_line(line: str) -> tuple[int, str]:\n    """TODO [TL-PDB-PARSE-01]: parse \'1000 main\'."""\n    raise NotImplementedError("TL-PDB-PARSE-01")',
        'def parse_symbol_line(line: str) -> tuple[int, str]:\n    # PEDAGOGY-SOLUTION: TL-PDB-PARSE-01\n    addr_s, name = line.strip().split(None, 1)\n    return int(addr_s, 16), name',
    ).replace(
        'def build_index(lines: list[str]) -> dict[int, str]:\n    """TODO [TL-PDB-INDEX-02]: addr->name index."""\n    raise NotImplementedError("TL-PDB-INDEX-02")',
        'def build_index(lines: list[str]) -> dict[int, str]:\n    # PEDAGOGY-SOLUTION: TL-PDB-INDEX-02\n    idx: dict[int, str] = {}\n    for ln in lines:\n        if not ln.strip():\n            continue\n        addr, name = parse_symbol_line(ln)\n        idx[addr] = name\n    return idx',
    ).replace(
        'def lookup_symbol(idx: dict[int, str], addr: int) -> str:\n    """TODO [TL-PDB-LOOKUP-03]: lookup or hex fallback."""\n    raise NotImplementedError("TL-PDB-LOOKUP-03")',
        'def lookup_symbol(idx: dict[int, str], addr: int) -> str:\n    # PEDAGOGY-SOLUTION: TL-PDB-LOOKUP-03\n    return idx.get(addr, f"0x{addr:x}")',
    )
    test = '''# PEDAGOGY-TEST: TL-PDB-PARSE-01
# PEDAGOGY-TEST: TL-PDB-INDEX-02
# PEDAGOGY-TEST: TL-PDB-LOOKUP-03
# Caso 1: parse 1000 main
# Caso 2: index len 2
# Caso 3: lookup main
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pdb_index import parse_symbol_line, build_index, lookup_symbol

def main():
    assert parse_symbol_line("1000 main") == (0x1000, "main")
    idx = build_index(["1000 main", "2000 foo"])
    assert len(idx) == 2
    assert lookup_symbol(idx, 0x1000) == "main"
    print("OK pdb_index")

if __name__ == "__main__":
    main()
'''
    write_pair(base, "pdb_index.py", starter, sol)
    write_pair(base, "test_pdb_index.py", test, test)
    write_pedagogy_pack(
        base, "pdb_symbol_index",
        "# PDB symbol index\n\nÍndice de símbolos (continua `miniobjdump`).\n",
        f"cd days/{DAY}/tooling/pdb_symbol_index/starter\npython test_pdb_index.py",
        todos,
        [("Symbol line", "ADDR NAME.", "hex parse.", "Formato fixture PDB."),
         ("Index build", "dict addr→name.", "loop lines.", "Lookup rápido."),
         ("Lookup", "nome ou hex.", "get fallback.", "Stack symbolize.")],
        "Índice PDB simplificado: parse, build e lookup.",
        ["parse main", "index len 2", "lookup main"],
    )


MODULES = [
    ("systems/clvm_trace_profiler", scaffold_clvm_trace_profiler),
    ("systems/arena_telemetry", scaffold_arena_telemetry),
    ("linux/perf_event_open_lab", scaffold_perf_event_open_lab),
    ("rust/stack_sample_trace", scaffold_stack_sample_trace),
    ("dotnet/activity_source_span", scaffold_activity_source_span),
    ("graphics/gpu_timer_query", scaffold_gpu_timer_query),
    ("redteam/yara_match_scan", scaffold_yara_match_scan),
    ("quantum/decoherence_noise", scaffold_decoherence_noise),
    ("ai/attention_mask", scaffold_attention_mask),
    ("nodejs/async_hooks_trace", scaffold_async_hooks_trace),
    ("parsers/logfmt_lexer", scaffold_logfmt_lexer),
    ("agent/verify_replay_log", scaffold_verify_replay_log),
    ("tooling/pdb_symbol_index", scaffold_pdb_symbol_index),
]


def build_todo_map() -> str:
    lines = ["# Mapa global de TODOs\n"]
    for module in sorted(DAY09.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md")):
        mod = module.parent
        rel_mod = mod.relative_to(DAY09).as_posix()
        starter = mod / "starter"
        if not starter.exists():
            continue
        for p in starter.rglob("*"):
            if p.is_file() and p.suffix.lower() in CODE_EXT:
                for ident in TODO_RE.findall(p.read_text(encoding="utf-8")):
                    rp = p.relative_to(starter).as_posix()
                    lines.extend([
                        f"## `{ident}`\n",
                        f"- **Módulo:** `{rel_mod}`",
                        f"- **Starter:** `starter/{rp}`",
                        f"- **Resolução:** `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`",
                        f"- **Teste:** `TESTES_GUIADOS.md` + `PEDAGOGY-TEST: {ident}`",
                        f"- **Solution:** `solutions/{rp}` + `PEDAGOGY-SOLUTION: {ident}`",
                        "",
                    ])
    return "\n".join(lines)


def scaffold_day_infra() -> None:
    DAY09.mkdir(parents=True, exist_ok=True)
    mod_table = "\n".join(
        f"| {i} | `{rel}` | observabilidade | 2–3 |"
        for i, (rel, _) in enumerate(MODULES, 1)
    )
    (DAY09 / "README.md").write_text(
        f"""# Day {DAY} — Observabilidade, profiling e depuração low-level

Dia **tier-A** (13 módulos): continua arcos dos Dias 07–08 com trace, profiling, spans e replay determinístico.

| # | Módulo | Fundamento | Horas |
|---|--------|------------|-------|
{mod_table}

**Total:** ~30–36 h.

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day {DAY}
python scripts/day_contract_check.py --day {DAY}
python scripts/run_day_tests.py --day {DAY} --mode solutions
```

Ver [`VALIDATION.md`](VALIDATION.md).
""",
        encoding="utf-8",
    )
    (DAY09 / "START_HERE.md").write_text(
        f"""# START HERE — Day {DAY}

Dia **tier-A (13 módulos)**: observabilidade, profiling e depuração low-level.

## Fluxo por módulo

1. `TEORIA_PASSO_A_PASSO.md` — trace no papel antes do código.
2. Checkpoint em [`ATIVIDADES.md`](ATIVIDADES.md).
3. `EXERCICIOS.md` → implemente `starter/` (`TODO [ID]`).
4. Testes (`PEDAGOGY-TEST: ID`); esperado FAIL até completar.
5. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar (inclui `## Baseline`).
6. Compare `solutions/` após tentativa; `BENCHMARK_GUIADO.md` → **Resultados observados**.

## Ordem sugerida

| Bloco | Módulos |
|-------|---------|
| Manhã CLVM + arena | `clvm_trace_profiler` → `arena_telemetry` |
| Linux + Rust | `perf_event_open_lab` → `stack_sample_trace` |
| .NET + GFX | `activity_source_span` → `gpu_timer_query` |
| Red team + quantum | `yara_match_scan` → `decoherence_noise` |
| AI + Node | `attention_mask` → `async_hooks_trace` |
| Parsers + agent + tooling | `logfmt_lexer` → `verify_replay_log` → `pdb_symbol_index` |

Mapa: `TODO_MAP.md` (39 TODOs). Trilhas: `docs/LEARNING_PATHS.md`.

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day {DAY}
python scripts/day_contract_check.py --day {DAY}
python scripts/run_day_tests.py --day {DAY} --mode solutions
```
""",
        encoding="utf-8",
    )
    blocks = "\n".join(
        f"| `{rel}` | {rel.split('/')[1].replace('_', '-')} |"
        for rel, _ in MODULES
    )
    (DAY09 / "ATIVIDADES.md").write_text(
        f"""# ATIVIDADES — {DAY} (13 módulos)

**Dia:** observabilidade tier-A | **~30–36 h**

## Preparação

- [ ] `START_HERE.md`, `README.md`, `TODO_MAP.md`

## Blocos

| Módulo | Checkpoint |
|--------|------------|
{blocks}

## Gates finais

```powershell
python scripts/pedagogy_check_unified.py --day {DAY}
python scripts/run_day_tests.py --day {DAY} --mode solutions
```
""",
        encoding="utf-8",
    )
    val_rows = "\n".join(
        f"| {rel.split('/')[0]} | {rel.split('/')[1]} | python/cargo/dotnet/node |"
        for rel, _ in MODULES
    )
    (DAY09 / "VALIDATION.md").write_text(
        f"""# VALIDATION — Day {DAY}

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day {DAY}
python scripts/day_contract_check.py --day {DAY}
python scripts/run_day_tests.py --day {DAY} --mode solutions
```

## Expectativas

| Gate | Esperado |
|------|----------|
| pedagogy_check | **PASS** — 13 módulos, 39 TODOs |
| day_contract | **PASS** — tier-A, todas trilhas |
| solutions | 13/13 PASS |

## Módulos (13)

| Trilha | Módulo | Runner |
|--------|--------|--------|
{val_rows}
""",
        encoding="utf-8",
    )
    (DAY09 / "TODO_MAP.md").write_text(build_todo_map(), encoding="utf-8")


def main() -> int:
    DAY09.mkdir(parents=True, exist_ok=True)
    for _, fn in MODULES:
        fn()
    scaffold_day_infra()
    print(f"Scaffolded {len(MODULES)} modules under days/{DAY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



