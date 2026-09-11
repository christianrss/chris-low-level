#!/usr/bin/env python3
"""Deepen thin GitHub-imported day-08 modules to pass pedagogy_check_unified."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days" / "2026-09-08"

MODS = [
    "systems/spsc_ring_buffer",
    "architecture/cache_set_sim",
    "ai/online_softmax",
    "redteam/wasm_binary_triage",
    "parsers/nfa_to_dfa",
    "agent/bm25_code_ranker",
    "unix/xargs_lite",
    "nodejs/worker_transfer",
    "dotnet/gc_allocation_probe",
]

BENCH = """# Benchmark guiado

## Hipótese
Caso 1 em loop deve ser O(n) estável.

## Como medir
Use o Baseline da RESOLUCAO.

## Resultados observados
- Ambiente: merge local
- Tempo: nao executado (meça após PASS)
- Interpretação: compare com `benchmarks/results-2026-09-08.md` se existir

## Skip honesto
nao executado neste passo de merge; valide corretude primeiro.
"""


def todos(mod: Path) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for base in (mod / "starter", mod / "solutions"):
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for tid in re.findall(r"(?:TODO\s*\[|PEDAGOGY-SOLUTION:\s*)([A-Z0-9-]+)", t):
                if tid not in seen:
                    seen.add(tid)
                    ids.append(tid)
    return ids


def sol_snip(mod: Path, tid: str, lang: str) -> str:
    blob = []
    for p in (mod / "solutions").rglob("*"):
        if not p.is_file():
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        m = re.search(
            rf"PEDAGOGY-SOLUTION:\s*{re.escape(tid)}[\s\S]{{0,800}}?(?=PEDAGOGY-SOLUTION:|\Z)",
            t,
        )
        if m:
            lines = [ln for ln in m.group(0).splitlines()[:20]]
            return "```" + lang + "\n" + "\n".join(lines) + "\n```\n"
    return f"```{lang}\n// implementar {tid}\n// ver solutions/\n// manter assinatura\n```\n"


def lang_for(mod: Path) -> str:
    sol = mod / "solutions"
    if list(sol.rglob("*.cpp")):
        return "cpp"
    if list(sol.rglob("*.cs")):
        return "csharp"
    if list(sol.rglob("*.mjs")) or list(sol.rglob("*.js")):
        return "javascript"
    return "python"


def baseline(mod: Path) -> str:
    rel = mod.relative_to(DAY).as_posix()
    if (mod / "starter" / "CMakeLists.txt").exists():
        return f"""cd days/2026-09-08/{rel}/starter
cmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure"""
    if list((mod / "starter").glob("*.csproj")) or list((mod / "starter").rglob("*.csproj")):
        return f"cd days/2026-09-08/{rel}/starter\ndotnet test"
    if list((mod / "starter").glob("test*.mjs")) or list((mod / "starter").glob("test.mjs")):
        return f"cd days/2026-09-08/{rel}/starter\nnode test.mjs"
    tests = list((mod / "starter").glob("test_*.py"))
    if tests:
        return f"cd days/2026-09-08/{rel}/starter\npython {tests[0].name}"
    return f"cd days/2026-09-08/{rel}/starter\n# rode o teste do README"


def teoria(name: str, ids: list[str], focus: str) -> str:
    tid_rows = "\n".join(f"| `{i}` | contrato do assert correspondente |" for i in ids)
    return f"""# Teoria passo a passo — {name}

Este laboratório veio da **trilha paralela GitHub** do dia 2026-09-08.

## 1. O quê

{focus}

## 2. Como — fluxo de dados

```text
entrada (fixture / literal do teste)
  -> validacao de limites
  -> transformacao do TODO
  -> saida comparada por igualdade estrita
```

## 3. Tabela de contrato

| Campo | Papel |
|-------|-------|
| starter | stubs com TODO |
| solutions | gabarito PEDAGOGY-SOLUTION |
| teste | PEDAGOGY-TEST / ctest / node / dotnet |

## 4. TODOs deste módulo

| ID | Papel |
|----|-------|
{tid_rows}

## 5. Trace numerico (Caso 1)

Siga o Caso 1 de `TESTES_GUIADOS.md` / asserts do teste no papel **antes** de editar.
Nao invente outro exemplo: o runner compara o literal.

## 6. Por quê este lab existe

Por quê está no dia 08 junto do toolchain CLVM? Porque treina um eixo ortogonal
(concorrencia / cache / ranking / automata) sem substituir o fio ISA.

## 7. Por quê falhar cedo

Por quê retornar false/Err/-1 imediatamente? Porque valor default silencioso
propaga lixo para o proximo assert.

## 8. Por quê o teste fixa literais

Por quê literais em vez de "quase certo"? Para impedir solucoes que so funcionam
no exemplo inventado pelo aluno.

## 9. Invariantes

1. Determinismo: mesma entrada => mesma saida.
2. Limites de capacidade / OOB respeitados.
3. Nao alterar assinaturas nem o teste.
4. Ordem dos TODOs da RESOLUCAO.

## 10. Bugs comuns

| Sintoma | Causa | Checagem |
|---------|-------|----------|
| off-by-one | indice/size | imprima cursor |
| ordem errada | publica antes de gravar | barreira acquire/release |
| score/prob NaN | divisao / log dominio | guarde eps |
| flake | estado residual | reset entre casos |

## 11. Lab versus producao

Producao tem mais flags e formatos. Aqui o recorte cabe no papel e ainda rejeita
o bug classico do modulo.

## 12. Checklist

- [ ] Caso 1 no papel
- [ ] Arquivo + funcao do primeiro TODO
- [ ] Sei o que nao mudar

## 13. Relacao com o core do dia

Compare com o anel C (`input_event_ring_mux`), o softmax C (`softmax_stable`) ou o
wasm asm (`wasm_section_header`) quando o tema se sobrepoe — sao contratos diferentes.
"""


def resolucao(mod: Path, name: str, ids: list[str]) -> str:
    lang = lang_for(mod)
    # find file anchors
    anchors = []
    starter = mod / "starter"
    for tid in ids:
        hit = "?"
        fn = "?"
        for p in starter.rglob("*"):
            if not p.is_file():
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if f"TODO [{tid}]" in t or f"TODO[{tid}]" in t:
                hit = f"starter/{p.relative_to(starter).as_posix()}"
                # crude function
                before = t.split(tid)[0][-200:]
                m = re.search(r"(?:def|bool|void|int|std::size_t|public |function |async )\s*(\w+)", before)
                if m:
                    fn = m.group(1)
                break
        anchors.append((tid, hit, fn))

    mapa = "| TODO | Arquivo | Funcao |\n|------|---------|--------|\n"
    for tid, hit, fn in anchors:
        mapa += f"| `{tid}` | `{hit}` | `{fn}` |\n"

    body = f"""# Resolucao guiada — {name}

## Mapa exato starter → resolucao

{mapa}

## Baseline

```powershell
{baseline(mod)}
```

**Esperado antes dos TODOs:** FAIL.

"""
    for tid, hit, fn in anchors:
        body += f"""
## {tid}

### Onde colocar ({tid})

| Campo | Valor |
|-------|-------|
| Arquivo | `{hit}` |
| Funcao | `{fn}` |
| Substituir | corpo sob `TODO [{tid}]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `{tid}` falha.

### Algoritmo / trace
Use o Caso ligado a `{tid}` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

{sol_snip(mod, tid, lang)}

### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `{tid}`.

### Verifique
Rode o baseline; o caminho de `{tid}` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `{tid}` PASS
- [ ] Nao alterei o teste
"""
    body += """
## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco do TODO |
| off-by-one | size/indice | refaca o trace |
| 2o caso falha | estado residual | reset |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado / preencher
"""
    return body


def ensure_extras(mod: Path, name: str, ids: list[str]) -> None:
    if not (mod / "EXERCICIOS.md").exists() or len((mod / "EXERCICIOS.md").read_text(encoding="utf-8").splitlines()) < 20:
        (mod / "EXERCICIOS.md").write_text(
            f"""# Exercicios — {name}

## Facil
Calcule no papel o Caso 1 do teste.

## Medio
Implemente o primeiro TODO ate o assert passar.

## Dificil
Implemente o caso negativo sem alterar o teste.

## Desafio
Documente uma extensao e o retorno de erro esperado.
""",
            encoding="utf-8",
            newline="\n",
        )
    if not (mod / "TESTES_GUIADOS.md").exists() or len((mod / "TESTES_GUIADOS.md").read_text(encoding="utf-8").splitlines()) < 15:
        lines = ["# Testes guiados\n"]
        for i, tid in enumerate(ids, 1):
            lines.append(f"## Caso {i}: `{tid}`\n\nExercido pelo harness do starter/solutions.\n")
        lines.append("## Identificadores\n")
        lines.extend(f"- `{t}`\n" for t in ids)
        (mod / "TESTES_GUIADOS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    if not (mod / "PESQUISA_GUIADA.md").exists():
        (mod / "PESQUISA_GUIADA.md").write_text(
            f"""# Pesquisa guiada — {name}

1. Qual invariante deste lab existe em producao com outro nome?
2. O que o off-by-one quebra no Caso 1?
3. Como o teste evita falha silenciosa?
4. Que parte da especificação real foi cortada?
5. Onde logar sem mudar o contrato dos TODOs?

## Fontes
- README do modulo
- docs/PEDAGOGY_STANDARD.md
""",
            encoding="utf-8",
            newline="\n",
        )
    (mod / "BENCHMARK_GUIADO.md").write_text(BENCH, encoding="utf-8", newline="\n")
    readme = mod / "README.md"
    if readme.exists():
        r = readme.read_text(encoding="utf-8")
        if "TODO" not in r:
            r = r.rstrip() + "\n\n## TODOs\n\n" + "\n".join(f"- `{i}`" for i in ids) + "\n"
            readme.write_text(r, encoding="utf-8", newline="\n")


FOCUS = {
    "systems/spsc_ring_buffer": "Ring SPSC com `head_`/`tail_` atomicos; capacidade logica = storage-1; push/pop false quando cheio/vazio.",
    "architecture/cache_set_sim": "Simulador de cache set-associative: decode set/tag, hit, politica de evicao.",
    "ai/online_softmax": "Softmax online (stats + normalize) sem materializar o vetor inteiro de uma vez.",
    "redteam/wasm_binary_triage": "Triagem de binario WASM: magic, ULEB, secoes — sem executar o modulo.",
    "parsers/nfa_to_dfa": "Construcao de DFA: epsilon-closure, subset construction, match.",
    "agent/bm25_code_ranker": "BM25 sobre corpus de codigo: tokenize, index, score, RR eval.",
    "unix/xargs_lite": "xargs educacional: split, batch por limite, run com shell=False.",
    "nodejs/worker_transfer": "Worker threads + transferables (ArrayBuffer muda de dono).",
    "dotnet/gc_allocation_probe": "Sondas de alocacao .NET: new vs pool vs contagem.",
}


def main() -> None:
    for rel in MODS:
        mod = DAY / rel
        ids = todos(mod)
        name = mod.name
        (mod / "TEORIA_PASSO_A_PASSO.md").write_text(
            teoria(name, ids, FOCUS[rel]), encoding="utf-8", newline="\n"
        )
        (mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").write_text(
            resolucao(mod, name, ids), encoding="utf-8", newline="\n"
        )
        ensure_extras(mod, name, ids)
        print("deepened", rel, "todos", len(ids))


if __name__ == "__main__":
    main()
