from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1];D=R/"days"/"2026-09-08";err=[];mods=0
req=["README.md","TEORIA_PASSO_A_PASSO.md","PESQUISA_GUIADA.md","RESOLUCAO_GUIADA_PASSO_A_PASSO.md","EXERCICIOS.md","TESTES_GUIADOS.md","BENCHMARK_GUIADO.md"]
for cat in D.iterdir():
 if not cat.is_dir():continue
 for m in cat.iterdir():
  if not m.is_dir():continue
  mods+=1
  for x in req:
   if not (m/x).exists():err.append(str(m/x))
  if not (m/"starter").exists() or not (m/"solutions").exists():err.append("starter/solution "+str(m))
if err:print("\n".join(err));sys.exit(1)
print(f"day06 quality check passed: {mods} modules")
