from __future__ import annotations
import re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'days'/'2026-09-04'
CODE_EXT={'.c','.cc','.cpp','.cxx','.h','.hpp','.py','.ts','.js','.cs','.rs','.asm','.s','.yar'}
TODO_RE=re.compile(r'TODO\s*\[([A-Z0-9-]+)\]')
UNTAGGED_RE=re.compile(r'(?:^|\s)(?://|#|/\*)\s*TODO\b(?!\s*\[[A-Z0-9-]+\])')

def text(p:Path)->str:return p.read_text(encoding='utf-8',errors='strict')
def main()->int:
 errors=[]; total=0
 modules=sorted(p.parent for p in DAY.glob('*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md'))
 if len(modules)!=11: errors.append(f'expected 11 Day02 modules, found {len(modules)}')
 for module in modules:
  rel=module.relative_to(ROOT)
  for req in ['TEORIA_PASSO_A_PASSO.md','PESQUISA_GUIADA.md','RESOLUCAO_GUIADA_PASSO_A_PASSO.md','TESTES_GUIADOS.md','starter','solutions']:
   if not (module/req).exists(): errors.append(f'{rel}: missing {req}')
  starter=module/'starter'; sol=module/'solutions'
  if not starter.exists() or not sol.exists(): continue
  res=text(module/'RESOLUCAO_GUIADA_PASSO_A_PASSO.md'); tg=text(module/'TESTES_GUIADOS.md')
  test_text='\n'.join(text(p) for p in (starter/'tests').rglob('*') if p.is_file()) if (starter/'tests').exists() else ''
  ids=[]
  for p in starter.rglob('*'):
   if not p.is_file() or p.suffix.lower() not in CODE_EXT: continue
   st=text(p); found=TODO_RE.findall(st)
   cleaned=TODO_RE.sub('',st)
   if 'TODO' in cleaned and UNTAGGED_RE.search(cleaned): errors.append(f'{rel}: untagged TODO in starter/{p.relative_to(starter)}')
   for ident in found:
    total+=1; ids.append(ident); rp=p.relative_to(starter); sp=sol/rp
    if not sp.exists(): errors.append(f'{rel}: TODO {ident} has no solutions/{rp}'); continue
    stsol=text(sp)
    if f'PEDAGOGY-SOLUTION: {ident}' not in stsol: errors.append(f'{rel}: {ident} missing solution marker in solutions/{rp}')
    if ident in TODO_RE.findall(stsol): errors.append(f'{rel}: {ident} remains TODO in solution/{rp}')
    if ident not in res: errors.append(f'{rel}: {ident} missing from resolution')
    if f'starter/{rp.as_posix()}' not in res: errors.append(f'{rel}: resolution does not name exact starter/{rp.as_posix()} for {ident}')
    if ident not in tg: errors.append(f'{rel}: {ident} missing from TESTES_GUIADOS')
    if f'PEDAGOGY-TEST: {ident}' not in test_text: errors.append(f'{rel}: {ident} missing actual test marker')
  if not ids: errors.append(f'{rel}: no tagged TODOs in starter')
  if len(ids)!=len(set(ids)): errors.append(f'{rel}: duplicate TODO IDs {ids}')
  low=res.lower()
  checks=[('debug/depur', ('debug','depur')), ('esperad', ('esperad',)), ('starter/', ('starter/',)), ('solutions/', ('solutions/',))]
  for label,needles in checks:
   if not any(n in low for n in needles): errors.append(f'{rel}: resolution missing operational section/token {label}')
  if 'bloco completo de loops está no gabarito' in low or 'bloco completo de loops esta no gabarito' in low:
   errors.append(f'{rel}: resolution still delegates essential implementation to solution')
  # CMake starters with tests must register CTest.
  if (starter/'CMakeLists.txt').exists() and (starter/'tests').exists():
   for label,base in [('starter',starter),('solutions',sol)]:
    cm=base/'CMakeLists.txt'
    if not cm.exists(): errors.append(f'{rel}: {label}/CMakeLists.txt missing'); continue
    c=text(cm)
    if 'enable_testing' not in c or 'add_test' not in c: errors.append(f'{rel}: {label} does not register tests')
 if errors:
  print('DAY02 PEDAGOGY CHECK FAILED')
  for e in errors: print(' -',e)
  return 1
 print(f'day02 pedagogy check passed: {len(modules)} modules, {total} starter TODO mappings')
 return 0
if __name__=='__main__': raise SystemExit(main())
