#!/usr/bin/env python3
"""Clean corrupted baselines and diversify high-dupe RESOLUCAO files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean_keep_contract(text: str) -> str:
    lines = []
    for ln in text.splitlines():
        if ln.strip() == "# keep contract / edge case":
            continue
        lines.append(ln)
    return "\n".join(lines) + "\n"


def fix_baseline_n(text: str) -> str:
    # starter\ndotnet / starter\nnode / starter\npython
    text = text.replace("starter\\ndotnet", "starter\ndotnet")
    text = text.replace("starter\\nnode", "starter\nnode")
    text = text.replace("starter\\npython", "starter\npython")
    text = text.replace("starter\\ncargo", "starter\ncargo")
    return text


PINNED = """# Resolucao guiada — pinned_memory_probe

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-DN-PIN` | `starter/Pinned.cs` | `SumPinned` |
| `D8-DN-LEN` | `starter/Pinned.cs` | `SumPinned` |
| `D8-DN-SUM` | `starter/Pinned.cs` | `SumPinned` |

## Baseline

```powershell
cd days/2026-09-10/dotnet/pinned_memory_probe/starter
dotnet test tests/Chris.PinnedLab.Tests.csproj
```

**Esperado antes dos TODOs:** FAIL.

## D8-DN-PIN

### Onde colocar (D8-DN-PIN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pinned.cs` |
| Funcao | `SumPinned` |
| Substituir | corpo sob `TODO [D8-DN-PIN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem pin, o GC pode mover o array enquanto o ponteiro e usado.

### Algoritmo / trace
1. `GCHandle.Alloc(data, Pinned)`.
2. Guarde o handle para `Free` no finally.
3. Nao some ainda — so estabilize a memoria.

### Escreva o codigo

```csharp
var handle = GCHandle.Alloc(data, GCHandleType.Pinned);
try {
    // next TODOs use handle / data
} finally {
    handle.Free();
}
```

### Por que funciona?
Pinned impede relocacao do objeto pelo GC durante o bloco.

### Verifique
Baseline parcial; `D8-DN-PIN` PASS.

### Checkpoint
- [ ] `D8-DN-PIN` PASS

## D8-DN-LEN

### Onde colocar (D8-DN-LEN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pinned.cs` |
| Funcao | `SumPinned` |
| Substituir | corpo sob `TODO [D8-DN-LEN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem `n = data.Length` o loop nao sabe o bound.

### Algoritmo / trace
1. Leia Length uma vez.
2. Use `n` no for (nao reconsultar Length a cada iteracao).
3. Confira com fixture `{1,2,3}` → n=3.

### Escreva o codigo

```csharp
int n = data.Length;
if (n < 0) {
    throw new InvalidOperationException("len");
}
```

### Por que funciona?
Fixa o bound antes da soma — contrato do assert de comprimento.

### Verifique
Baseline parcial; `D8-DN-LEN` PASS.

### Checkpoint
- [ ] `D8-DN-LEN` PASS

## D8-DN-SUM

### Onde colocar (D8-DN-SUM)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pinned.cs` |
| Funcao | `SumPinned` |
| Substituir | corpo sob `TODO [D8-DN-SUM]` |
| Nao mexer | assinatura / testes |

### O problema
Sem acumular bytes o teste espera soma errada.

### Algoritmo / trace
1. `s = 0`.
2. Para i em [0,n): `s += data[i]`.
3. Retorne s (ex.: 1+2+3=6).

### Escreva o codigo

```csharp
int s = 0;
for (int i = 0; i < n; i++) {
    s += data[i];
}
return s;
```

### Por que funciona?
Soma linear dos bytes no intervalo pinado.

### Verifique
Baseline completo; `D8-DN-SUM` PASS.

### Checkpoint
- [ ] `D8-DN-SUM` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| AccessViolation | Free cedo | Free so no finally |
| soma 0 | loop vazio | confira n |
| GC move | sem Alloc | PIN primeiro |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes: pin enquanto le
- Edge cases: array vazio
- Benchmark: nao executado
"""

CTX = """# Resolucao guiada — context_budgeter

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-CTX-SCORE` | `starter/context_budgeter.py` | `base_score` |
| `D9-CTX-DEDUPE` | `starter/context_budgeter.py` | `pack` |
| `D9-CTX-DIVERSITY` | `starter/context_budgeter.py` | `pack` |
| `D9-CTX-BUDGET` | `starter/context_budgeter.py` | `pack` |

## Baseline

```powershell
cd days/2026-09-11/agent/context_budgeter/starter
python test_context_budgeter.py
```

**Esperado antes dos TODOs:** FAIL.

## D9-CTX-SCORE

### Onde colocar (D9-CTX-SCORE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/context_budgeter.py` |
| Funcao | `base_score` |
| Substituir | corpo sob `TODO [D9-CTX-SCORE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem score ponderado o ranking fica arbitrario.

### Algoritmo / trace
1. Pegue lexical/semantic/graph do candidato.
2. Combine 0.45 / 0.35 / 0.20.
3. Retorne float.

### Escreva o codigo

```python
def base_score(c):
    return 0.45 * c["lexical"] + 0.35 * c["semantic"] + 0.20 * c["graph"]
```

### Por que funciona?
Contrato numerico do ranking base antes de diversity/budget.

### Verifique
`D9-CTX-SCORE` PASS no harness.

### Checkpoint
- [ ] `D9-CTX-SCORE` PASS

## D9-CTX-DEDUPE

### Onde colocar (D9-CTX-DEDUPE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/context_budgeter.py` |
| Funcao | `pack` |
| Substituir | corpo sob `TODO [D9-CTX-DEDUPE]` |
| Nao mexer | assinatura / testes |

### O problema
Conteudo duplicado consome budget sem ganho.

### Algoritmo / trace
1. Normalize CRLF/trailing spaces por linha.
2. SHA-256 do texto normalizado.
3. Se hash ja visto → trace duplicate; senao append.

### Escreva o codigo

```python
unique, seen, trace = [], set(), []
for c in candidates:
    norm = "\\n".join(line.rstrip() for line in c["content"].splitlines())
    h = hashlib.sha256(norm.encode()).hexdigest()
    if h in seen:
        trace.append({"path": c["path"], "decision": "duplicate"})
        continue
    seen.add(h)
    x = dict(c)
    x["_base"] = base_score(c)
    unique.append(x)
```

### Por que funciona?
Hash estavel remove clones antes de gastar bytes.

### Verifique
`D9-CTX-DEDUPE` PASS.

### Checkpoint
- [ ] `D9-CTX-DEDUPE` PASS

## D9-CTX-DIVERSITY

### Onde colocar (D9-CTX-DIVERSITY)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/context_budgeter.py` |
| Funcao | `pack` |
| Substituir | corpo sob `TODO [D9-CTX-DIVERSITY]` |
| Nao mexer | assinatura / testes |

### O problema
Sem bonus de path novo o pack vicia no mesmo arquivo.

### Algoritmo / trace
1. Escolha max por (base + 0.05 se path novo, -bytes, path).
2. Remova de remaining.
3. Atualize paths set ao selecionar.

### Escreva o codigo

```python
chosen, paths, used = [], set(), 0
remaining = unique[:]
while remaining:
    best = max(
        remaining,
        key=lambda c: (c["_base"] + (0.05 if c["path"] not in paths else 0), -c["bytes"], c["path"]),
    )
    remaining.remove(best)
    effective = best["_base"] + (0.05 if best["path"] not in paths else 0)
```

### Por que funciona?
Diversity bonus favorece paths ainda nao usados.

### Verifique
`D9-CTX-DIVERSITY` PASS.

### Checkpoint
- [ ] `D9-CTX-DIVERSITY` PASS

## D9-CTX-BUDGET

### Onde colocar (D9-CTX-BUDGET)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/context_budgeter.py` |
| Funcao | `pack` |
| Substituir | corpo sob `TODO [D9-CTX-BUDGET]` |
| Nao mexer | assinatura / testes |

### O problema
Sem corte por bytes o pack estoura o contexto.

### Algoritmo / trace
1. Se used+bytes > budget → over_budget continue.
2. Senao append selected, used += bytes, paths.add.
3. Retorne selected/used/trace.

### Escreva o codigo

```python
    if used + best["bytes"] > budget:
        trace.append({"path": best["path"], "decision": "over_budget", "effective": effective})
        continue
    chosen.append({k: v for k, v in best.items() if not k.startswith("_")})
    used += best["bytes"]
    paths.add(best["path"])
    trace.append({"path": best["path"], "decision": "selected", "effective": effective})
return {"selected": chosen, "used": used, "trace": trace}
```

### Por que funciona?
Hard cap de bytes com audit trail por decisao.

### Verifique
`D9-CTX-BUDGET` PASS; pack completo.

### Checkpoint
- [ ] `D9-CTX-BUDGET` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| duplicates passam | hash errado | normalize antes |
| sempre mesmo path | sem bonus | diversity |
| used > budget | sem check | BUDGET |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes: used <= budget
- Edge cases: all duplicates
- Benchmark: nao executado
"""


def main() -> None:
    for day in ("2026-09-09", "2026-09-10", "2026-09-11"):
        for p in (ROOT / "days" / day).rglob("RESOLUCAO_GUIADA_PASSO_A_PASSO.md"):
            t = p.read_text(encoding="utf-8")
            nt = fix_baseline_n(clean_keep_contract(t))
            if nt != t:
                p.write_text(nt, encoding="utf-8", newline="\n")
                print("cleaned", p.relative_to(ROOT))
    (ROOT / "days/2026-09-10/dotnet/pinned_memory_probe/RESOLUCAO_GUIADA_PASSO_A_PASSO.md").write_text(
        PINNED, encoding="utf-8", newline="\n"
    )
    # CTX has intentional \\n in python string for join — write carefully
    ctx_path = ROOT / "days/2026-09-11/agent/context_budgeter/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    # In the fence we need real backslash-n for the Python source shown
    ctx = CTX.replace(
        'norm = "\\\\n".join',
        'norm = "\\n".join',
    )
    ctx_path.write_text(ctx, encoding="utf-8", newline="\n")
    print("rewrote pinned + context_budgeter")


if __name__ == "__main__":
    main()
