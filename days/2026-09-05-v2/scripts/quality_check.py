from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
errs=[]; files=[]
for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    files.append(p)
    rel=p.relative_to(ROOT)
    if '__pycache__' in p.parts or p.suffix=='.pyc': errs.append(f'cache artifact: {rel}')
    if any((part.startswith('build') or part=='_build_matmul') for part in rel.parts[:-1]): errs.append(f'build artifact: {rel}')
    if p.suffix.lower() in {'.exe','.o','.obj','.so','.dll','.a'}: errs.append(f'binary artifact: {rel}')
    if p.suffix.lower() in {'.md','.py','.cpp','.c','.h','.hpp','.js','.cs','.sh','.json'}:
        try: text=p.read_text(encoding='utf-8')
        except Exception: continue
        for n,line in enumerate(text.splitlines(),1):
            if len(line)>800: errs.append(f'long line {rel}:{n} ({len(line)})')
print(f'files_scanned={len(files)}')
if errs:
    print('\n'.join('ERROR '+e for e in errs)); sys.exit(1)
print('QUALITY CHECK PASS')
