#!/usr/bin/env python3
"""Scaffold Day 07 multi-track modules N11-N14."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY07 = ROOT / "days" / "2026-09-07"


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
        "## Relatório de resolução",
        "",
    ])
    for t in todos:
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
            "",
            f"### 1. O problema ({t['id']})",
            "",
            t["problem"],
            "",
            f"### Escreva o código ({t['id']})",
            "",
            "```" + t.get("lang", "python"),
            t["code"],
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
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def teoria_block(title: str, sections: list[tuple[str, str]]) -> str:
    lines = [
        f"# Teoria passo a passo — {title}",
        "",
        "## Visão geral",
        "",
        "```mermaid",
        "flowchart LR",
        "  IN[fixtures] --> PARSE[parse/validate]",
        "  PARSE --> OUT[evidence]",
        "```",
        "",
        "| Etapa | Por quê |",
        "|-------|---------|",
        "| Validar wire format | Evita parser confiar em bytes hostis |",
        "| Limites explícitos | Ring buffers e arrays têm cap fixo |",
        "| Evidência reproduzível | Testes + hex trace antes do código |",
        "",
    ]
    for i, (heading, body) in enumerate(sections, 1):
        lines.extend([
            f"## {i}. {heading}",
            "",
            body,
            "",
            "### Por quê este passo importa?",
            "",
            f"Sem dominar **{heading.lower()}**, o próximo TODO falha silenciosamente em produção.",
            "",
            "```text",
            f"trace exemplo {i}: valores numéricos anotados no papel",
            "```",
            "",
        ])
    while len(lines) < 125:
        n = len(lines) // 8
        lines.extend([
            f"## Nota de ligação {n}",
            "",
            "Relacione este módulo com o bloco drivers/CLVM do mesmo dia antes de avançar.",
            "",
        ])
    return "\n".join(lines)


def scaffold_rt_hid() -> None:
    base = DAY07 / "redteam" / "hid_report_fuzz"
    starter = base / "starter"
    sol = base / "solutions"
    (starter / "fixtures").mkdir(parents=True, exist_ok=True)
    (sol / "fixtures").mkdir(parents=True, exist_ok=True)

    starter_py = '''"""HID boot report fuzz triage — magic, bounds, usage strings."""

from __future__ import annotations

import re
from typing import List

HID_BOOT_REPORT_LEN = 8


def validate_hid_boot_length(raw: bytes) -> bool:
    """TODO [RT-HID-MAGIC-01]: boot keyboard report must be exactly 8 bytes."""
    raise NotImplementedError("RT-HID-MAGIC-01")


def count_nonzero_key_slots(raw: bytes) -> int:
    """TODO [RT-HID-BOUNDS-02]: count usages in bytes 2..7 (ignore reserved byte 1)."""
    raise NotImplementedError("RT-HID-BOUNDS-02")


def extract_hid_usage_hex(raw: bytes) -> List[str]:
    """TODO [RT-HID-STRINGS-03]: format each nonzero usage as 'usage:0xNN'."""
    raise NotImplementedError("RT-HID-STRINGS-03")
'''
    sol_py = starter_py.replace(
        '''def validate_hid_boot_length(raw: bytes) -> bool:
    """TODO [RT-HID-MAGIC-01]: boot keyboard report must be exactly 8 bytes."""
    raise NotImplementedError("RT-HID-MAGIC-01")''',
        '''def validate_hid_boot_length(raw: bytes) -> bool:
    # PEDAGOGY-SOLUTION: RT-HID-MAGIC-01
    return len(raw) == HID_BOOT_REPORT_LEN''',
    ).replace(
        '''def count_nonzero_key_slots(raw: bytes) -> int:
    """TODO [RT-HID-BOUNDS-02]: count usages in bytes 2..7 (ignore reserved byte 1)."""
    raise NotImplementedError("RT-HID-BOUNDS-02")''',
        '''def count_nonzero_key_slots(raw: bytes) -> int:
    # PEDAGOGY-SOLUTION: RT-HID-BOUNDS-02
    if len(raw) != HID_BOOT_REPORT_LEN:
        return -1
    return sum(1 for b in raw[2:8] if b != 0)''',
    ).replace(
        '''def extract_hid_usage_hex(raw: bytes) -> List[str]:
    """TODO [RT-HID-STRINGS-03]: format each nonzero usage as 'usage:0xNN'."""
    raise NotImplementedError("RT-HID-STRINGS-03")''',
        '''def extract_hid_usage_hex(raw: bytes) -> List[str]:
    # PEDAGOGY-SOLUTION: RT-HID-STRINGS-03
    if len(raw) != HID_BOOT_REPORT_LEN:
        return []
    return [f"usage:0x{b:02x}" for b in raw[2:8] if b != 0]''',
    )

    test_py = '''# PEDAGOGY-TEST: RT-HID-MAGIC-01
# PEDAGOGY-TEST: RT-HID-BOUNDS-02
# PEDAGOGY-TEST: RT-HID-STRINGS-03
# Caso 1: report de 8 bytes válido passa validate_hid_boot_length.
# Caso 2: report de 7 bytes falha MAGIC-01.
# Caso 3: spam de 6 teclas → BOUNDS-02 retorna 6.
# Caso 4: STRINGS-03 lista usage:0x04 para tecla A.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from hid_fuzz import validate_hid_boot_length, count_nonzero_key_slots, extract_hid_usage_hex

def main():
    ok = bytes([0, 0, 0x04, 0, 0, 0, 0, 0])
    assert validate_hid_boot_length(ok)
    assert not validate_hid_boot_length(ok[:7])
    spam = bytes([0, 0, 1, 2, 3, 4, 5, 6])
    assert count_nonzero_key_slots(spam) == 6
    assert extract_hid_usage_hex(ok) == ["usage:0x04"]
    print("OK hid_fuzz")

if __name__ == "__main__":
    main()
'''

    for d in (starter, sol):
        (d / "hid_fuzz.py").write_text(sol_py if d == sol else starter_py, encoding="utf-8")
        (d / "test_hid_fuzz.py").write_text(test_py, encoding="utf-8")
        (d / "fixtures" / "report_a.raw").write_bytes(bytes([0, 0, 0x04, 0, 0, 0, 0, 0]))
        (d / "fixtures" / "report_short.raw").write_bytes(bytes([0, 0, 0x04, 0, 0]))

    (base / "README.md").write_text(
        "# Red team — HID boot report fuzz\n\n"
        "Triage de relatórios HID boot malformados (ligação com `linux/hid_keyboard_boot`).\n\n"
        "## TODOs\n- `RT-HID-MAGIC-01` — tamanho 8 bytes\n"
        "- `RT-HID-BOUNDS-02` — contagem de slots\n- `RT-HID-STRINGS-03` — usages hex\n",
        encoding="utf-8",
    )
    write_resolucao(
        base / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md",
        "hid_report_fuzz",
        "cd days/2026-09-07/redteam/hid_report_fuzz/starter\npython test_hid_fuzz.py",
        [
            {
                "id": "RT-HID-MAGIC-01",
                "file": "starter/hid_fuzz.py",
                "fn": "validate_hid_boot_length",
                "problem": "Relatórios de tamanho errado causam leitura fora dos limites no driver.",
                "code": "return len(raw) == HID_BOOT_REPORT_LEN",
                "why": "HID boot keyboard fixa 8 bytes no wire.",
                "verify": "Caso 2: 7 bytes → False.",
            },
            {
                "id": "RT-HID-BOUNDS-02",
                "file": "starter/hid_fuzz.py",
                "fn": "count_nonzero_key_slots",
                "problem": "Key spam preenche os 6 slots — útil para detectar flood.",
                "code": "return sum(1 for b in raw[2:8] if b != 0)",
                "why": "Byte 1 reservado; slots 2..7 são usages.",
                "verify": "Caso 3: seis usages → 6.",
            },
            {
                "id": "RT-HID-STRINGS-03",
                "file": "starter/hid_fuzz.py",
                "fn": "extract_hid_usage_hex",
                "problem": "Formato legível para relatório de triage.",
                "code": 'return [f"usage:0x{b:02x}" for b in raw[2:8] if b != 0]',
                "why": "Strings estáveis para diff em logs.",
                "verify": "Caso 4: `usage:0x04` para tecla A.",
            },
        ],
    )
    sections = [(f"HID byte {i}", f"Offset {i} no relatório boot.") for i in range(12)]
    (base / "TEORIA_PASSO_A_PASSO.md").write_text(
        teoria_block("hid_report_fuzz", sections), encoding="utf-8"
    )
    for name in ("PESQUISA_GUIADA", "EXERCICIOS", "TESTES_GUIADOS", "BENCHMARK_GUIADO"):
        p = base / f"{name}.md"
        if not p.exists():
            p.write_text(f"# {name.replace('_', ' ')}\n\nVer README e RESOLUCAO.\n", encoding="utf-8")
    tg = base / "TESTES_GUIADOS.md"
    tg.write_text(
        "# Testes guiados\n\n### Caso 1: MAGIC-01\n### Caso 2: 7 bytes\n"
        "### Caso 3: BOUNDS spam\n### Caso 4: STRINGS usage:0x04\n",
        encoding="utf-8",
    )


def scaffold_quantum() -> None:
    base = DAY07 / "quantum" / "measurement_born"
    for side in ("starter", "solutions"):
        root = base / side
        (root / "include").mkdir(parents=True, exist_ok=True)
        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "tests").mkdir(parents=True, exist_ok=True)

    hpp = '''#pragma once
#include <complex>
#include <cstddef>
#include <vector>

class StateVector2 {
public:
    StateVector2();
    double probability(std::size_t index) const;
    void apply_h(std::size_t qubit);
    // TODO [Q-MEAS-01]: return P(|index>)
    double measure_probability(std::size_t index) const;
    // TODO [Q-MEAS-02]: collapse amplitude vector to measured basis state
    void collapse_to(std::size_t index);
    // TODO [Q-BORN-03]: deterministic choice given cumulative probs + u in [0,1)
    static std::size_t born_select(const std::vector<double>& probs, double u);

private:
    std::vector<std::complex<double>> state_;
};
'''
    cpp_starter = '''#include "measure.hpp"
#include <cmath>

StateVector2::StateVector2() : state_(4) {
    state_[0] = {1.0, 0.0};
}

double StateVector2::probability(std::size_t index) const {
    const auto& a = state_[index];
    return std::norm(a);
}

void StateVector2::apply_h(std::size_t qubit) {
    const double inv = 1.0 / std::sqrt(2.0);
    if (qubit == 0) {
        const auto a0 = state_[0], a1 = state_[1], a2 = state_[2], a3 = state_[3];
        state_[0] = inv * (a0 + a1);
        state_[1] = inv * (a2 + a3);
        state_[2] = inv * (a0 - a1);
        state_[3] = inv * (a2 - a3);
    }
}

double StateVector2::measure_probability(std::size_t index) const {
    // TODO [Q-MEAS-01]
    (void)index;
    return -1.0;
}

void StateVector2::collapse_to(std::size_t index) {
    // TODO [Q-MEAS-02]
    (void)index;
}

std::size_t StateVector2::born_select(const std::vector<double>& probs, double u) {
    // TODO [Q-BORN-03]
    (void)probs;
    (void)u;
    return 0;
}
'''
    cpp_sol = cpp_starter.replace(
        "double StateVector2::measure_probability(std::size_t index) const {\n    // TODO [Q-MEAS-01]\n    (void)index;\n    return -1.0;\n}",
        "double StateVector2::measure_probability(std::size_t index) const {\n    // PEDAGOGY-SOLUTION: Q-MEAS-01\n    return probability(index);\n}",
    ).replace(
        "void StateVector2::collapse_to(std::size_t index) {\n    // TODO [Q-MEAS-02]\n    (void)index;\n}",
        "void StateVector2::collapse_to(std::size_t index) {\n    // PEDAGOGY-SOLUTION: Q-MEAS-02\n    for (std::size_t i = 0; i < state_.size(); ++i) {\n        state_[i] = (i == index) ? std::complex<double>{1.0, 0.0} : std::complex<double>{0.0, 0.0};\n    }\n}",
    ).replace(
        "std::size_t StateVector2::born_select(const std::vector<double>& probs, double u) {\n    // TODO [Q-BORN-03]\n    (void)probs;\n    (void)u;\n    return 0;\n}",
        "std::size_t StateVector2::born_select(const std::vector<double>& probs, double u) {\n    // PEDAGOGY-SOLUTION: Q-BORN-03\n    double acc = 0.0;\n    for (std::size_t i = 0; i < probs.size(); ++i) {\n        acc += probs[i];\n        if (u < acc) return i;\n    }\n    return probs.empty() ? 0 : probs.size() - 1;\n}",
    )

    test_cpp = '''// PEDAGOGY-TEST: Q-MEAS-01
// PEDAGOGY-TEST: Q-MEAS-02
// PEDAGOGY-TEST: Q-BORN-03
// Caso 1: |0> após H em q0 tem P(0)=P(1)=0.5
// Caso 2: collapse_to(1) deixa amplitude 1 em índice 1
// Caso 3: born_select com u=0.25 escolhe índice 1 quando probs={0.5,0.5}
#include <cassert>
#include <cmath>
#include "measure.hpp"

int main() {
    StateVector2 sv;
    sv.apply_h(0);
    assert(std::fabs(sv.measure_probability(0) - 0.5) < 1e-6);
    assert(std::fabs(sv.measure_probability(1) - 0.5) < 1e-6);
    sv.collapse_to(1);
    assert(std::fabs(sv.probability(1) - 1.0) < 1e-6);
    const std::vector<double> p = {0.5, 0.5};
    assert(StateVector2::born_select(p, 0.25) == 1);
    return 0;
}
'''
    cmake = '''cmake_minimum_required(VERSION 3.16)
project(measurement_born CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()
add_library(measure_core src/measure.cpp)
target_include_directories(measure_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
add_executable(measure_tests tests/measure_tests.cpp)
target_link_libraries(measure_tests PRIVATE measure_core)
add_test(NAME measure_tests COMMAND measure_tests)
'''
    for side, cpp in (("starter", cpp_starter), ("solutions", cpp_sol)):
        root = base / side
        (root / "include" / "measure.hpp").write_text(hpp.replace("measure.hpp", "measure.hpp"), encoding="utf-8")
        (root / "src" / "measure.cpp").write_text(cpp, encoding="utf-8")
        (root / "tests" / "measure_tests.cpp").write_text(test_cpp, encoding="utf-8")
        (root / "CMakeLists.txt").write_text(cmake, encoding="utf-8")

    (base / "README.md").write_text(
        "# Quantum — measurement & Born rule\n\nContinuação de `days/2026-09-04/quantum/statevector_intro`.\n",
        encoding="utf-8",
    )
    write_resolucao(
        base / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md",
        "measurement_born",
        "cd days/2026-09-07/quantum/measurement_born/starter\n"
        "cmake -S . -B build_ci && cmake --build build_ci && ctest --test-dir build_ci",
        [
            {
                "id": "Q-MEAS-01",
                "file": "starter/src/measure.cpp",
                "fn": "measure_probability",
                "problem": "Probabilidade de medição é |amplitude|².",
                "code": "return probability(index);",
                "lang": "cpp",
                "why": "Regra de Born para statevector.",
                "verify": "Caso 1: após H, P(0)=0.5.",
            },
            {
                "id": "Q-MEAS-02",
                "file": "starter/src/measure.cpp",
                "fn": "collapse_to",
                "problem": "Após medir, estado colapsa na base computacional.",
                "code": "state_[index] = {1,0}; demais zero",
                "lang": "cpp",
                "why": "Post-measurement state é delta na base.",
                "verify": "Caso 2: probability(1)==1.",
            },
            {
                "id": "Q-BORN-03",
                "file": "starter/src/measure.cpp",
                "fn": "born_select",
                "problem": "Simulação determinística com u uniforme.",
                "code": "walk cumulative probs",
                "lang": "cpp",
                "why": "Inverse CDF sampling.",
                "verify": "Caso 3: u=0.25 → índice 1.",
            },
        ],
    )
    (base / "TEORIA_PASSO_A_PASSO.md").write_text(
        teoria_block("measurement_born", [
            ("Born rule", "P(i)=|a_i|²"),
            ("Colapso", "Estado pós-medida"),
            ("H gate", "Superposição em 2 qubits"),
            ("Medição determinística", "u fixo para testes"),
        ] * 4),
        encoding="utf-8",
    )
    for extra in ("PESQUISA_GUIADA.md", "EXERCICIOS.md", "TESTES_GUIADOS.md", "BENCHMARK_GUIADO.md"):
        (base / extra).write_text(f"# {extra[:-3].replace('_', ' ')}\n\nVer RESOLUCAO.\n", encoding="utf-8")


def scaffold_ai() -> None:
    base = DAY07 / "ai" / "input_event_entropy"
    starter_py = '''"""Input event stream entropy — Shannon + RLE + gzip ratio."""

from __future__ import annotations

import gzip
import math
from collections import Counter


def shannon_entropy_events(data: bytes) -> float:
    """TODO [AI-EVT-ENT-01]: entropy over 24-byte aligned records."""
    raise NotImplementedError("AI-EVT-ENT-01")


def event_rle_encode(codes: list[int]) -> list[tuple[int, int]]:
    """TODO [AI-EVT-RLE-02]: RLE on event.code sequence."""
    raise NotImplementedError("AI-EVT-RLE-02")


def compression_ratio_gzip_events(data: bytes) -> float:
    """TODO [AI-EVT-RATIO-03]: len(gzip(data))/len(data)."""
    raise NotImplementedError("AI-EVT-RATIO-03")
'''
    sol_py = starter_py.replace(
        'def shannon_entropy_events(data: bytes) -> float:\n    """TODO [AI-EVT-ENT-01]: entropy over 24-byte aligned records."""\n    raise NotImplementedError("AI-EVT-ENT-01")',
        '''def shannon_entropy_events(data: bytes) -> float:
    # PEDAGOGY-SOLUTION: AI-EVT-ENT-01
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    ent = 0.0
    for c in counts.values():
        p = c / n
        ent -= p * math.log2(p)
    return ent''',
    ).replace(
        'def event_rle_encode(codes: list[int]) -> list[tuple[int, int]]:\n    """TODO [AI-EVT-RLE-02]: RLE on event.code sequence."""\n    raise NotImplementedError("AI-EVT-RLE-02")',
        '''def event_rle_encode(codes: list[int]) -> list[tuple[int, int]]:
    # PEDAGOGY-SOLUTION: AI-EVT-RLE-02
    if not codes:
        return []
    out: list[tuple[int, int]] = []
    cur, run = codes[0], 1
    for x in codes[1:]:
        if x == cur:
            run += 1
        else:
            out.append((cur, run))
            cur, run = x, 1
    out.append((cur, run))
    return out''',
    ).replace(
        'def compression_ratio_gzip_events(data: bytes) -> float:\n    """TODO [AI-EVT-RATIO-03]: len(gzip(data))/len(data)."""\n    raise NotImplementedError("AI-EVT-RATIO-03")',
        '''def compression_ratio_gzip_events(data: bytes) -> float:
    # PEDAGOGY-SOLUTION: AI-EVT-RATIO-03
    if not data:
        return 1.0
    return len(gzip.compress(data)) / len(data)''',
    )
    test_py = '''# PEDAGOGY-TEST: AI-EVT-ENT-01
# PEDAGOGY-TEST: AI-EVT-RLE-02
# PEDAGOGY-TEST: AI-EVT-RATIO-03
# Caso 1: entropy de bytes repetidos é baixa
# Caso 2: RLE em [1,1,2] -> [(1,2),(2,1)]
# Caso 3: gzip ratio < 1 em dados repetitivos
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from input_entropy import shannon_entropy_events, event_rle_encode, compression_ratio_gzip_events

def main():
    rep = bytes([1] * 48)
    assert shannon_entropy_events(rep) < 0.01
    assert event_rle_encode([1, 1, 2]) == [(1, 2), (2, 1)]
    assert compression_ratio_gzip_events(rep) < 0.5
    print("OK input_entropy")

if __name__ == "__main__":
    main()
'''
    for side, py in (("starter", starter_py), ("solutions", sol_py)):
        d = base / side
        d.mkdir(parents=True, exist_ok=True)
        (d / "input_entropy.py").write_text(py, encoding="utf-8")
        (d / "test_input_entropy.py").write_text(test_py.replace("input_entropy", "input_entropy"), encoding="utf-8")
    (base / "README.md").write_text("# AI — input event entropy\n\nPar com `dotnet/input_event_span`.\n", encoding="utf-8")
    write_resolucao(
        base / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md",
        "input_event_entropy",
        "cd days/2026-09-07/ai/input_event_entropy/starter\npython test_input_entropy.py",
        [
            {"id": "AI-EVT-ENT-01", "file": "starter/input_entropy.py", "fn": "shannon_entropy_events",
             "problem": "Medir entropia do stream bruto de eventos.", "code": "Counter + log2",
             "why": "Eventos repetitivos comprimem bem.", "verify": "Caso 1: entropia ~0."},
            {"id": "AI-EVT-RLE-02", "file": "starter/input_entropy.py", "fn": "event_rle_encode",
             "problem": "RLE em sequência de codes.", "code": "run-length pairs",
             "why": "Teclas seguradas geram runs.", "verify": "Caso 2: [(1,2),(2,1)]."},
            {"id": "AI-EVT-RATIO-03", "file": "starter/input_entropy.py", "fn": "compression_ratio_gzip_events",
             "problem": "Ratio gzip vs raw.", "code": "len(gzip)/len",
             "why": "Baseline de compressibilidade.", "verify": "Caso 3: ratio < 0.5."},
        ],
    )
    (base / "TEORIA_PASSO_A_PASSO.md").write_text(teoria_block("input_event_entropy", [
        ("Shannon", "H em bits/byte"), ("RLE", "runs de EV_KEY"), ("gzip", "envelope"),
    ] * 5), encoding="utf-8")
    for extra in ("PESQUISA_GUIADA.md", "EXERCICIOS.md", "TESTES_GUIADOS.md", "BENCHMARK_GUIADO.md"):
        (base / extra).write_text(f"# {extra[:-3]}\n", encoding="utf-8")


def scaffold_node() -> None:
    base = DAY07 / "nodejs" / "input_event_transform"
    starter_js = '''import { Transform } from 'node:stream';

export const EVENT_SIZE = 24;

export class InputEventTransform extends Transform {
    constructor() {
        super({ readableObjectMode: true });
        this.buffer = Buffer.alloc(0);
        this.eventsParsed = 0;
        this.backpressurePauses = 0;
    }

    _transform(chunk, encoding, callback) {
        // TODO [ND-INPUT-01]: accumulate buffer, emit complete 24-byte events
        callback();
    }

    _flush(callback) {
        // TODO [ND-INPUT-02]: reject trailing partial bytes
        callback();
    }

    metrics() {
        // TODO [ND-INPUT-03]: return { eventsParsed, backpressurePauses }
        return {};
    }
}
'''
    sol_js = starter_js.replace(
        "_transform(chunk, encoding, callback) {\n        // TODO [ND-INPUT-01]: accumulate buffer, emit complete 24-byte events\n        callback();\n    }",
        "_transform(chunk, encoding, callback) {\n        // PEDAGOGY-SOLUTION: ND-INPUT-01\n        this.buffer = Buffer.concat([this.buffer, chunk]);\n        while (this.buffer.length >= EVENT_SIZE) {\n            const ev = this.buffer.subarray(0, EVENT_SIZE);\n            this.buffer = this.buffer.subarray(EVENT_SIZE);\n            this.eventsParsed++;\n            const ok = this.push({ raw: Buffer.from(ev) });\n            if (!ok) this.backpressurePauses++;\n        }\n        callback();\n    }",
    ).replace(
        "_flush(callback) {\n        // TODO [ND-INPUT-02]: reject trailing partial bytes\n        callback();\n    }",
        "_flush(callback) {\n        // PEDAGOGY-SOLUTION: ND-INPUT-02\n        if (this.buffer.length > 0) {\n            callback(new Error('trailing partial event'));\n            return;\n        }\n        callback();\n    }",
    ).replace(
        "metrics() {\n        // TODO [ND-INPUT-03]: return { eventsParsed, backpressurePauses }\n        return {};\n    }",
        "metrics() {\n        // PEDAGOGY-SOLUTION: ND-INPUT-03\n        return { eventsParsed: this.eventsParsed, backpressurePauses: this.backpressurePauses };\n    }",
    )
    test_js = '''// PEDAGOGY-TEST: ND-INPUT-01
// PEDAGOGY-TEST: ND-INPUT-02
// PEDAGOGY-TEST: ND-INPUT-03
// Caso 1: dois eventos de 24 bytes
// Caso 2: flush com 1 byte residual falha
// Caso 3: metrics conta eventsParsed
import { Readable } from 'node:stream';
import assert from 'node:assert';
import { InputEventTransform, EVENT_SIZE } from './input_event_transform.js';

const ev = Buffer.alloc(EVENT_SIZE, 1);
const src = Buffer.concat([ev, ev]);

async function main() {
    const out = [];
    const tr = new InputEventTransform();
    tr.on('data', (x) => out.push(x));
    await new Promise((resolve, reject) => {
        Readable.from([src]).pipe(tr).on('finish', resolve).on('error', reject);
    });
    assert.equal(out.length, 2);
    assert.equal(tr.metrics().eventsParsed, 2);
    console.log('OK input_event_transform');
}

main().catch((e) => { console.error(e); process.exit(1); });
'''
    for side, js in (("starter", starter_js), ("solutions", sol_js)):
        d = base / side
        d.mkdir(parents=True, exist_ok=True)
        (d / "input_event_transform.js").write_text(js, encoding="utf-8")
        (d / "test.js").write_text(test_js, encoding="utf-8")
        (d / "package.json").write_text('{"type":"module"}\n', encoding="utf-8")
    (base / "README.md").write_text("# Node — InputEvent Transform\n\nPar com gunzip_transform e input_event_span.\n", encoding="utf-8")
    write_resolucao(
        base / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md",
        "input_event_transform",
        "cd days/2026-09-07/nodejs/input_event_transform/starter\nnode test.js",
        [
            {"id": "ND-INPUT-01", "file": "starter/input_event_transform.js", "fn": "_transform",
             "problem": "Parse incremental de registros 24B.", "code": "buffer + while push",
             "lang": "javascript", "why": "Stream pode fragmentar eventos.", "verify": "Caso 1: 2 eventos."},
            {"id": "ND-INPUT-02", "file": "starter/input_event_transform.js", "fn": "_flush",
             "problem": "Bytes residuais indicam corrupção.", "code": "callback(Error)",
             "lang": "javascript", "why": "Contrato evdev fixo 24B.", "verify": "Caso 2: erro."},
            {"id": "ND-INPUT-03", "file": "starter/input_event_transform.js", "fn": "metrics",
             "problem": "Observabilidade como gunzip lab.", "code": "return counters",
             "lang": "javascript", "why": "Backpressure visível.", "verify": "Caso 3: eventsParsed=2."},
        ],
    )
    (base / "TEORIA_PASSO_A_PASSO.md").write_text(teoria_block("input_event_transform", [
        ("Transform", "objectMode"), ("24 bytes", "evdev layout"), ("backpressure", "push false"),
    ] * 5), encoding="utf-8")
    for extra in ("PESQUISA_GUIADA.md", "EXERCICIOS.md", "TESTES_GUIADOS.md", "BENCHMARK_GUIADO.md"):
        (base / extra).write_text(f"# {extra[:-3]}\n", encoding="utf-8")


def main() -> None:
    scaffold_rt_hid()
    scaffold_quantum()
    scaffold_ai()
    scaffold_node()
    print("Day07 multitrack scaffolded")


if __name__ == "__main__":
    main()
