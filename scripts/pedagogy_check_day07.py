from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[1];D=R/"days"/"2026-09-09";errs=[];ids=[]
for p in D.rglob("*"):
    if p.is_file() and "starter" in p.parts:
        txt=p.read_text(errors="ignore")
        for tid in re.findall(r"TODO \[([A-Z0-9-]+)\]",txt):
            ids.append(tid); rel=p.relative_to(D); mod=D/rel.parts[0]/rel.parts[1]
            res=mod/"RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
            if not res.exists() or tid not in res.read_text(errors="ignore"): errs.append("resolution "+tid)
            if not any(f"PEDAGOGY-TEST: {tid}" in q.read_text(errors="ignore") for q in (mod/"starter").rglob("*") if q.is_file()): errs.append("test "+tid)
            if not any(f"PEDAGOGY-SOLUTION: {tid}" in q.read_text(errors="ignore") for q in (mod/"solutions").rglob("*") if q.is_file()): errs.append("solution "+tid)
if len(ids)!=len(set(ids)): errs.append("duplicate ids")
for p in D.rglob("RESOLUCAO_GUIADA_PASSO_A_PASSO.md"):
    words=len(re.findall(r"\b\w+\b",p.read_text(errors="ignore")))
    if words<120: errs.append(f"resolution too short {p}: {words}")
if errs: print("\n".join(errs));sys.exit(1)
print(f"day07 pedagogy check passed: {len(ids)} TODO mappings")
