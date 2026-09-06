# Lantern Hunt

FPS horror didático em OpenGL (Win32/WGL): dungeon procedural, texturas + normal maps, lanterna spotlight, áudio ambiente/passos, insetos e coleta de comida.

## Build (Windows + MSVC)

```powershell
python tools/generate_assets.py
cmake -S . -B build -A x64
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Executáveis:

| Target | Descrição |
|--------|-----------|
| `lantern_hunt` | **solutions/** — jogo completo |
| `lantern_hunt_starter` | **starter/** — stubs com TODOs |
| `test_procgen` | seed determinística |
| `test_collision` | colisão AABB sem GPU |

## Controles

| Tecla | Ação |
|-------|------|
| WASD | mover |
| Mouse | olhar |
| Clique | atirar gude |
| R | nova seed |
| Esc | sair |

## Estrutura

```text
assets/          texturas PNG + WAV (CC0 gerados)
docs/            (vazio — material pedagógico na raiz do módulo)
TEORIA_*.md      teoria, exercícios, resolução, testes (raiz)
solutions/       gabarito jogável
starter/         implementação do aluno (TODO LANTERN-*)
third_party/     stb_image.h, miniaudio.h
tools/           generate_assets.py, gen_normal_from_height.py
```

Comece em [`START_HERE.md`](START_HERE.md).
