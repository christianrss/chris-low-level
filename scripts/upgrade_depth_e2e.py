#!/usr/bin/env python3
"""Bulk upgrade for end-to-end depth: porting, pesquisa, test cases, benchmarks."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from module_project_map import MODULE_PROJECT, module_key

ROOT = Path(__file__).resolve().parents[1]

PESQUISA_WORKSHEET = """

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
"""

PORTING_SECTION = """

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `{project}` |
| O que levar | {carry} |
| Testes a replicar | {tests} |
| Milestone | {milestone} |
| Commit sugerido | `{commit}` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
"""

REAL_ENV_MODULES = {
    "2026-09-05/linux/kernel_module_driver_lab": """## Execução real (opcional)

**Pré-requisitos:** Linux com headers do kernel, `build-essential`, VM recomendada.

```bash
python scripts/run_real_env_checklist.py --module linux/kernel_module_driver_lab --day 2026-09-05
```

Correlacione `device_set_trace(1)` no userspace com `dmesg` após `insmod`.
""",
    "2026-09-03/boot/legacy_bootsector": """## Execução real (opcional)

**Pré-requisitos:** NASM, QEMU (`qemu-system-x86_64`).

```bash
python scripts/run_real_env_checklist.py --module boot/legacy_bootsector --day 2026-09-03
```
""",
    "2026-09-05/dotnet/cil_tiny_decoder": """## Execução real (opcional)

**Pré-requisitos:** .NET SDK 8+.

```bash
python scripts/run_real_env_checklist.py --module dotnet/cil_tiny_decoder --day 2026-09-05
```
""",
    "2026-09-05/linux/distro_pkg_rootfs": """## Execução real (opcional)

**Pré-requisitos:** Linux, `bash`, permissão para criar diretórios temporários.

```bash
python scripts/run_real_env_checklist.py --module linux/distro_pkg_rootfs --day 2026-09-05
```
""",
}

BENCH_DAY01: dict[str, str] = {
    "architecture/toy_cpu": "| MIPS (5000×130 instr) | ~123 | chris-cpu benchmark |",
    "p2p/gossip": "| Broadcast 2000 peers | ~2.5 ms | deliveries=2000 |",
    "network/http_parser": "| HTTP parse throughput | ~1.67M req/s | 200k requests |",
    "terminal/ansi_parser": "| Parser throughput | ~447 MiB/s | 20 MiB input |",
    "hardware/descriptor_ring": "| Descriptors/s | ~104M | 2M completed |",
    "blockchain/toy_chain": "| PoW diff=2 median | ~0.82 ms | nonce ~192 |",
    "assembly/x86_64_abi_sum": "| C vs ASM loop | 0.012s vs 0.024s | ASM slower at tiny N |",
    "systems/clvm": "| VM run median | ~1.18 ms | includes startup |",
    "tooling/miniobjdump": "| Disasm median | ~1.28 ms | includes startup |",
    "ai/linear_autograd": "| Python train step | ~0.51 ms | 50 runs median |",
    "graphics/dual_backend_3d": "| Core update | ~163 ns/iter | 1M iterations |",
    "redteam/benign_reversing": "| Scan 1–8 MiB | ~16.3 MiB/s | binary toolkit |",
    "boot/legacy_bootsector": "| Layout test | N/A (byte model) | QEMU opcional |",
}


def find_modules(day_dir: Path) -> list[Path]:
    return sorted(p.parent for p in day_dir.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def ensure_section(path: Path, marker: str, content: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    path.write_text(text.rstrip() + content, encoding="utf-8")
    return True


def upgrade_pesquisa(module: Path) -> bool:
    p = module / "PESQUISA_GUIADA.md"
    return ensure_section(p, "## Registro do aluno", PESQUISA_WORKSHEET)


def upgrade_porting(day: str, module: Path) -> bool:
    rel = module.relative_to(ROOT / "days" / day).as_posix()
    key = module_key(day, rel)
    info = MODULE_PROJECT.get(key)
    if not info:
        return False
    section = PORTING_SECTION.format(**info)
    return ensure_section(module / "README.md", "## Portar para projects/", section)


def upgrade_testes_guiados(module: Path) -> bool:
    p = module / "TESTES_GUIADOS.md"
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8")
    if "### Caso 1" in text or "## Caso 1" in text:
        return False
    lines = text.splitlines()
    out: list[str] = []
    case_num = 0
    for line in lines:
        stripped = line.strip()
        if re.match(r"^\d+\.\s+", stripped) and not stripped.startswith("#"):
            case_num += 1
            body = re.sub(r"^\d+\.\s+", "", stripped)
            out.append(f"### Caso {case_num}: {body}")
        elif stripped.startswith("**") and stripped.endswith("**") and ":" in stripped:
            case_num += 1
            title = stripped.strip("*")
            out.append(f"### Caso {case_num}: {title}")
        else:
            out.append(line)
    if case_num == 0:
        return False
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    return True


def sync_test_case_comments(module: Path) -> int:
    """Use repair_pedagogy_depth.py for test case comment blocks."""
    return 0


def upgrade_benchmark_day01(module: Path, rel: str) -> bool:
    row = BENCH_DAY01.get(rel)
    if not row:
        return False
    p = module / "BENCHMARK_GUIADO.md"
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8")
    if "não executado" not in text.lower() and "nao executado" not in text.lower():
        return False
    replacement = f"""## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
{row}

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.
"""
    text = re.sub(
        r"## Resultados observados\n.*",
        replacement.strip(),
        text,
        flags=re.DOTALL,
    )
    p.write_text(text, encoding="utf-8")
    return True


def add_real_env(day: str, module: Path) -> bool:
    rel = module.relative_to(ROOT / "days" / day).as_posix()
    key = module_key(day, rel)
    block = REAL_ENV_MODULES.get(key)
    if not block:
        return False
    return ensure_section(module / "TESTES_GUIADOS.md", "## Execução real (opcional)", "\n" + block)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", action="append", default=[])
    parser.add_argument("--all-days", action="store_true")
    args = parser.parse_args()

    days = args.day or []
    if args.all_days:
        days = sorted(
            p.name for p in (ROOT / "days").iterdir()
            if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", p.name)
        )

    stats = {"pesquisa": 0, "porting": 0, "testes": 0, "tests_sync": 0, "bench": 0, "real": 0}
    for day in days:
        day_dir = ROOT / "days" / day
        for module in find_modules(day_dir):
            rel = module.relative_to(day_dir).as_posix()
            if upgrade_pesquisa(module):
                stats["pesquisa"] += 1
            if upgrade_porting(day, module):
                stats["porting"] += 1
            if upgrade_testes_guiados(module):
                stats["testes"] += 1
            stats["tests_sync"] += sync_test_case_comments(module)
            if day == "2026-09-03" and upgrade_benchmark_day01(module, rel):
                stats["bench"] += 1
            if add_real_env(day, module):
                stats["real"] += 1

    print("upgrade_depth_e2e:", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
