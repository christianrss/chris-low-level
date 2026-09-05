from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; bad=[];count=0
for p in ROOT.rglob('*'):
 if p.is_file() and '.git' not in p.parts:
  count+=1
  if p.stat().st_size==0: bad.append(str(p))
  if p.suffix in {'.md','.py','.js','.c','.cpp','.hpp','.cs','.sh','.json'}:
   try:p.read_text(encoding='utf-8')
   except Exception as e:bad.append(f'{p}: {e}')
if bad: print('\n'.join(bad));sys.exit(1)
print(f'quality files checked: {count}'); print('quality check passed')
