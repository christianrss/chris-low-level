# BENCHMARK_GUIADO — Lantern Hunt

## Métrica alvo (dia estendido)

| Métrica | Meta | Método |
|---------|------|--------|
| FPS médio (só 3D) | ≥ 45 | 60 s em dungeon 32×32, solutions |
| FPS médio (3D + HUD + menu) | ≥ 42 | mesma sessão com HUD sempre ligado |
| Frame time p95 | < 25 ms | mesma sessão |
| `test_procgen` | < 50 ms | `Measure-Command` |
| `test_collision` | < 30 ms | `Measure-Command` |
| `test_objectives` | < 20 ms | `Measure-Command` |
| `test_checkpoint` | < 80 ms | `Measure-Command` (inclui `game_reset`) |

---

## Procedimento FPS (mundo 3D)

1. Build Release: `cmake --build build --config Release`
2. Feche apps pesadas na GPU.
3. Execute `lantern_hunt.exe`; entre no jogo (seed 42); ande pelo mapa 60 s.
4. Meça com contador OS/OBS (título da janela não inclui FPS nativo).

---

## Overhead HUD / menu / overlay

O pipeline desenha **depois** da cena 3D:

```text
cena 3D (N × glDrawArrays) → draw_slime_overlay → HudRenderer::draw → MenuRenderer (se não Playing)
```

### Por quê documentar separado?

- **Slime overlay:** um quad fullscreen com blend — custo baixo (~0.1 ms) mas overdraw total.
- **Font bitmap (`font.cpp`):** cada glyph usa vários `glBegin`/`glEnd` — em HUD completo (barras + 3 linhas de texto + modo água/gosma), espere **1–4 ms** em GPU integrada.
- **Menu:** menos geometria que HUD em jogo, mas texto grande (scale 2.0) aumenta quads.

### Medição sugerida (A/B)

1. **Baseline A:** comente temporariamente `g_hud.draw` e `draw_slime_overlay` em `solutions/src/main_win32.cpp` → meça FPS 60 s.
2. **Baseline B:** reative HUD apenas → delta de FPS.
3. **Baseline C:** menu em `MainMenu` 60 s (sem simulação) → custo quase só clear + texto.

Preencha:

| Modo | FPS médio | Delta vs A |
|------|-----------|------------|
| A — só 3D | ___ | — |
| B — 3D + HUD + slime | ___ | ___ |
| C — menu estático | ___ | N/A |

**Nota pedagógica:** se B cai abaixo de 42 FPS mas A ≥ 45, o gargalo do dia 1 é **immediate mode 2D**, não procgen nem colisão — candidato a atlas + VBO no dia 2.

---

## Timing dos 4 testes (PowerShell)

```powershell
cd days/2026-09-06/graphics/lantern_hunt/build/Release

Measure-Command { .\test_procgen.exe } | Select-Object TotalMilliseconds
Measure-Command { .\test_collision.exe } | Select-Object TotalMilliseconds
Measure-Command { .\test_objectives.exe } | Select-Object TotalMilliseconds
Measure-Command { .\test_checkpoint.exe } | Select-Object TotalMilliseconds
```

Ou loop para média:

```powershell
Measure-Command { 1..50 | ForEach-Object { .\test_procgen.exe } }
```

### Resultado observado (preencher)

| Teste | ms (1 run) | ms (50 run média) | Notas |
|-------|------------|-------------------|-------|
| test_procgen | ___ | ___ | dominado por loop O(n²) de assert |
| test_collision | ___ | ___ | |
| test_objectives | ___ | ___ | |
| test_checkpoint | ___ | ___ | inclui generate_dungeon |

**Esperado:** procgen pura dentro de `generate_dungeon` < 1 ms; tempo total de `test_procgen` maior por comparar 32×32 células duas vezes.

---

## Micro-benchmark procgen isolado

Para medir só geração (sem test harness), adicione temporariamente em `test_procgen.cpp`:

```cpp
#include <chrono>
auto t0 = std::chrono::steady_clock::now();
for (int i = 0; i < 1000; ++i) { lantern::generate_dungeon(42u); }
auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
std::cout << "1000 dungeons: " << ms << " ms\n";
```

Remova antes de commitar.

---

## Resultados observados

| Data | GPU | FPS 3D | FPS 3D+HUD | Notas |
|------|-----|--------|------------|-------|
| 2026-09-06 | (preencher) | n/a | n/a | cubos por célula, sem instancing |

---

## Resultado FPS detalhado (opcional)

---

## Por quê medir?

- Grid 32×32 com chão + parede + água + entidades → **milhares** de draw calls — baseline para instancing no dia 2.
- Os 4 testes `ctest` garantem regressão **CPU** enquanto você otimiza **GPU**.
- Separar overhead HUD evita “otimizar procgen” quando o limite real é `glBegin` no texto.

---

## Próximos passos (após benchmark)

1. Instancing para chão/parede por `SurfaceKind`
2. Font atlas em textura única + um draw call para HUD
3. Unificar slime overlay com shader pós-process (dia 3+)
