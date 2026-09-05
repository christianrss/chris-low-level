from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    "ai/linear_autograd",
    "architecture/toy_cpu",
    "assembly/x86_64_abi_sum",
    "blockchain/toy_chain",
    "boot/legacy_bootsector",
    "graphics/dual_backend_3d",
    "hardware/descriptor_ring",
    "network/http_parser",
    "p2p/gossip",
    "redteam/benign_reversing",
    "systems/clvm",
    "terminal/ansi_parser",
    "tooling/miniobjdump"
]
required = ['README.md','TEORIA_PASSO_A_PASSO.md','EXERCICIOS.md',
            'RESOLUCAO_GUIADA_PASSO_A_PASSO.md','BENCHMARK_GUIADO.md']
errs = []
todo_count = 0
for rel in MODULES:
    m = ROOT / rel
    for f in required:
        if not (m / f).is_file():
            errs.append(f'{rel}: missing {f}')
    teor = (m / 'TEORIA_PASSO_A_PASSO.md').read_text(encoding='utf-8', errors='ignore')
    if len(teor.splitlines()) < 120:
        errs.append(f'{rel}: TEORIA < 120 lines ({len(teor.splitlines())})')
    ex = (m / 'EXERCICIOS.md').read_text(encoding='utf-8', errors='ignore')
    for lvl in ['Fácil', 'Médio', 'Difícil', 'Desafio']:
        if lvl not in ex:
            errs.append(f'{rel}: EXERCICIOS missing {lvl}')
    res = (m / 'RESOLUCAO_GUIADA_PASSO_A_PASSO.md').read_text(encoding='utf-8', errors='ignore')
    if len(res.splitlines()) < 80:
        errs.append(f'{rel}: RESOLUCAO < 80 lines ({len(res.splitlines())})')
    if '## Relatório de resolução' not in res:
        errs.append(f'{rel}: missing Relatório de resolução')
    bench = (m / 'BENCHMARK_GUIADO.md').read_text(encoding='utf-8', errors='ignore')
    if '## Resultados observados' not in bench:
        errs.append(f'{rel}: missing Resultados observados')
    starter = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in (m/'starter').rglob('*') if p.is_file())
    ids = sorted(set(re.findall(r'TODO \[([A-Z0-9-]+)\]', starter)))
    tests = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in (m/'starter').rglob('*') if p.is_file() and 'test' in p.name.lower())
    for tid in ids:
        todo_count += 1
        if f'PEDAGOGY-TEST [{tid}]' not in tests:
            errs.append(f'{rel}: {tid} missing PEDAGOGY-TEST')
print(f'modules={len(MODULES)} todo_mappings={todo_count}')
if errs:
    print('\n'.join('ERROR '+e for e in errs))
    sys.exit(1)
print('PEDAGOGY CHECK PASS')
