from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[1];D=R/"days"/"2026-09-08";err=[];seen=[]
for p in D.rglob("*"):
 if p.is_file() and "starter" in p.parts:
  txt=p.read_text(errors="ignore")
  for tid in re.findall(r"TODO \[([A-Z0-9-]+)\]",txt):
   seen.append(tid); rel=p.relative_to(D); mod=D/rel.parts[0]/rel.parts[1]
   res=(mod/"RESOLUCAO_GUIADA_PASSO_A_PASSO.md").read_text(errors="ignore")
   if tid not in res:err.append("resolution "+tid)
   if not any(f"PEDAGOGY-TEST: {tid}" in q.read_text(errors="ignore") for q in (mod/"starter").rglob("*") if q.is_file()):err.append("test "+tid)
   if not any(f"PEDAGOGY-SOLUTION: {tid}" in q.read_text(errors="ignore") for q in (mod/"solutions").rglob("*") if q.is_file()):err.append("solution "+tid)
if len(seen)!=len(set(seen)):err.append("duplicate TODO ids")
if err: print("\n".join(err));sys.exit(1)
print(f"day06 pedagogy check passed: {len(seen)} TODO mappings")
