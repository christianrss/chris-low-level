from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
mods=sorted((ROOT/'modules').iterdir())
required=['README.md','TEORIA_PASSO_A_PASSO.md','PESQUISA_GUIADA.md','EXERCICIOS.md','RESOLUCAO_GUIADA_PASSO_A_PASSO.md','TESTES_GUIADOS.md','BENCHMARK_GUIADO.md','GABARITO.md']
errs=[]; todo_count=0
for m in mods:
    if not m.is_dir(): continue
    for f in required:
        if not (m/f).is_file(): errs.append(f'{m.name}: missing {f}')
    if not (m/'starter').is_dir() or not (m/'solutions').is_dir(): errs.append(f'{m.name}: missing starter/solutions'); continue
    starter='\n'.join(p.read_text(errors='ignore') for p in (m/'starter').rglob('*') if p.is_file())
    ids=sorted(set(re.findall(r'TODO \[([A-Z0-9-]+)\]',starter)))
    # also allow multiple ids in one TODO MAPPING line
    ids=sorted(set(ids)|set(re.findall(r'\[([A-Z][A-Z0-9-]+-\d+)\]',starter)))
    res=(m/'RESOLUCAO_GUIADA_PASSO_A_PASSO.md').read_text()
    tests='\n'.join(p.read_text(errors='ignore') for p in (m/'starter').rglob('*') if p.is_file() and ('test' in p.name.lower())) + '\n' + '\n'.join(p.read_text(errors='ignore') for p in (m/'solutions').rglob('*') if p.is_file() and ('test' in p.name.lower() or p.name=='Program.cs'))
    sol='\n'.join(p.read_text(errors='ignore') for p in (m/'solutions').rglob('*') if p.is_file())
    for tid in ids:
        todo_count+=1
        if tid not in res: errs.append(f'{m.name}: {tid} absent from resolution')
        if tid not in tests and 'SOURCE-REVIEW' not in tid: errs.append(f'{m.name}: {tid} absent from tests')
        if tid not in sol: errs.append(f'{m.name}: {tid} absent from solution')
    if not ids: errs.append(f'{m.name}: no TODO ids found')
print(f'modules={len(mods)} todo_mappings={todo_count}')
if errs:
    print('\n'.join('ERROR '+e for e in errs)); sys.exit(1)
print('PEDAGOGY CHECK PASS')
