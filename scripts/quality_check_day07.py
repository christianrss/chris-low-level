from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1];D=R/"days"/"2026-09-09";err=[];mods=0
req=["README.md","TEORIA_PASSO_A_PASSO.md","PESQUISA_GUIADA.md","EXERCICIOS.md","RESOLUCAO_GUIADA_PASSO_A_PASSO.md","TESTES_GUIADOS.md","BENCHMARK_GUIADO.md"]
for cat in D.iterdir():
    if not cat.is_dir(): continue
    for mod in cat.iterdir():
        if not mod.is_dir():continue
        mods+=1
        for f in req:
            if not (mod/f).exists() or (mod/f).stat().st_size==0:err.append(f"missing {mod/f}")
        if not (mod/"starter").exists() or not (mod/"solutions").exists():err.append(f"starter/solution {mod}")
if err:print("\n".join(err));sys.exit(1)
print(f"day07 quality check passed: {mods} modules")
