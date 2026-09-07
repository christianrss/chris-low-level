# ATIVIDADES — 2026-09-03

**Dia:** 13 módulos | **~8–12 h** (escolha trilhas)  
**Regra:** trace no papel antes de `starter/`. Ver `START_HERE.md`.

## Ordem sugerida

1. `architecture/toy_cpu` → `assembly/x86_64_abi_sum`
2. `systems/clvm` ou `tooling/miniobjdump`
3. Duas trilhas: `graphics/dual_backend_3d`, `network/http_parser`, etc.
4. `redteam/benign_reversing`

## Checkpoints

- [ ] Trace fetch/decode/execute em `toy_cpu`
- [ ] Um frame CPU vs GL documentado em `dual_backend_3d`
- [ ] Hexdump de 16 bytes de `.clvm` ou ELF

## Síntese

1. O que ABI e calling convention têm a ver com `clvm` loader?
2. Por que parser incremental (HTTP/ANSI) não pode assumir buffer completo?
3. Próximo capstone: `projects/chris-vm` ou `projects/chris-http`?
