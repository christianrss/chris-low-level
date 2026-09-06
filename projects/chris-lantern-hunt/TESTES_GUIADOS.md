# TESTES_GUIADOS — Lantern Hunt

Testes automáticos (sem GPU) e checklist manual (GPU + áudio + HUD).

## Mapa TODO → teste

| TODO | Evidência | Tipo |
|------|-----------|------|
| LANTERN-PROC-01 | Caso 1 — `test_procgen.exe` | automático |
| LANTERN-WATER-12 | Caso 2 — `water_count()` em `test_procgen` | automático |
| LANTERN-CAM-02 | Caso 3 — `test_collision.exe` | automático |
| LANTERN-OBJ-17 | Caso 4 — `test_objectives.exe` | automático |
| LANTERN-CHK-16 | Caso 5 — `test_checkpoint.exe` | automático |
| LANTERN-TEX-02 | Checklist #5 (texturas no chão) | manual GPU |
| LANTERN-NORM-03 | Checklist #5 (relevo na parede) | manual GPU |
| LANTERN-LIGHT-04 | Checklist #5 (cone estreito) | manual GPU |
| LANTERN-AUDIO-08 | Checklist #2–3 | manual áudio |
| LANTERN-PROJ-05 | Checklist #9 | manual GPU |
| LANTERN-HIT-06 | Checklist #9 | manual GPU |
| LANTERN-AI-07 | Checklist #9 + insetos em parede | manual GPU |
| LANTERN-PICKUP-09 | Checklist #10 | manual GPU |
| LANTERN-PLACE-10 | 5 comidas + 12 insetos seed 42 | manual GPU |
| LANTERN-SLIME-11 | Checklist #8 | manual GPU |
| LANTERN-FONT-13 | Checklist #1 (título menu) | manual GPU |
| LANTERN-HUD-14 | Checklist #6–7 | manual GPU |
| LANTERN-MENU-15 | Checklist #1, #13–14 | manual GPU |

Marcadores: `starter/tests/pedagogy_registry.cpp` + arquivos em `solutions/tests/`.

---

## Testes automáticos (sem GPU)

### Caso 1 — Procgen seed 42 (`LANTERN-PROC-01`)

**Comando:**
```powershell
.\build\Release\test_procgen.exe
```

**Esperado:** `test_procgen: PASS seed=42 floors=... rooms=...`

**Asserts:**
- Duas gerações com seed `42` → células idênticas
- `rooms.size() >= 6`, `floor_count() >= 180`

**Código:** `solutions/tests/test_procgen.cpp` — `PEDAGOGY-TEST: LANTERN-PROC-01`

---

### Caso 2 — Água na procgen (`LANTERN-WATER-12`)

**Comando:** mesmo `test_procgen.exe` (Caso 1 inclui assert de água).

**Esperado:** `water_count() >= 8` para seed `42`.

**Código:** `solutions/tests/test_procgen.cpp` — comentário `Caso 3 — seed 42 inclui água`

**Nota:** no starter, este assert **falha** até `carve_water_pool` em `procgen.cpp`.

---

### Caso 3 — Colisão slide (`LANTERN-CAM-02`)

**Comando:**
```powershell
.\build\Release\test_collision.exe
```

**Esperado:** `test_collision: PASS`

**Código:** `solutions/tests/test_collision.cpp` — `PEDAGOGY-TEST: LANTERN-CAM-02`

---

### Caso 4 — Objetivos (`LANTERN-OBJ-17`)

**Comando:**
```powershell
.\build\Release\test_objectives.exe
```

**Esperado:** `test_objectives: PASS`

**Fluxo testado:** 3 salas → comida 5 → 4 insetos → checkpoint → escape ready → `all_complete()`.

**Código:** `solutions/tests/test_objectives.cpp` — `PEDAGOGY-TEST: LANTERN-OBJ-17`

---

### Caso 5 — Checkpoint (`LANTERN-CHK-16`)

**Comando:**
```powershell
.\build\Release\test_checkpoint.exe
```

**Esperado:** `test_checkpoint: PASS`

**Fluxo testado:** `game_reset` → altera vida/posição → `checkpoint_save` → restore → campos iguais.

**Código:** `solutions/tests/test_checkpoint.cpp` — `PEDAGOGY-TEST: LANTERN-CHK-16`

---

## CTest (4 testes registrados)

```powershell
cd build
ctest -C Release --output-on-failure
```

| Nome CTest | Executável | TODO principal |
|------------|------------|----------------|
| `lantern_procgen_seed42` | `test_procgen` | PROC-01 + WATER-12 |
| `lantern_collision_slide` | `test_collision` | CAM-02 |
| `lantern_objectives_flow` | `test_objectives` | OBJ-17 |
| `lantern_checkpoint_save` | `test_checkpoint` | CHK-16 |

---

## Checklist manual (GPU + áudio + UI)

| # | Passo | Esperado | TODO relacionado |
|---|-------|----------|------------------|
| 1 | Abrir `lantern_hunt_starter.exe` | Menu principal com título bitmap | MENU-15, FONT-13 |
| 2 | Enter “Jogar (seed 42)” | Dungeon carrega, ambiente sonoro | PROC-01, AUDIO-08 |
| 3 | WASD 5 s | Passos audíveis (~2–3/s máx) | AUDIO-08 |
| 4 | Mover mouse | Câmera gira | CAM-02 (movimento) |
| 5 | Olhar parede com lanterna | Relevo visível | NORM-03, LIGHT-04 |
| 6 | HUD canto inferior | Barra VIDA vermelha | HUD-14 |
| 7 | Encontrar lago | Água azul; barra RESPIRACAO | WATER-12, HUD-14 |
| 8 | Pisar gosma verde | Overlay verde + lentidão | SLIME-11 |
| 9 | Clique em inseto | Tiro + inseto eliminado | PROJ-05, HIT-06 |
| 10 | Coletar 5 comidas | `COMIDA 5/5` | PICKUP-09 |
| 11 | Tecla E no altar | Altar brilha; checkpoint salvo | CHK-16 |
| 12 | Completar 5 objetivos | Tela VITORIA | OBJ-17 |
| 13 | Esc no jogo | Overlay PAUSADO | MENU-15 |
| 14 | Game Over → Enter | Volta ao menu | MENU-15 |
| 15 | Tecla R (se implementado) | Novo layout sem crash | E11 |

---

## Checklist HUD / menu (detalhado)

### HUD em jogo (`LANTERN-HUD-14`)
- [ ] Barra de vida proporcional a `health / 100`
- [ ] Barra de respiração **só** quando `water != None`
- [ ] Linha `COMIDA x/5` atualiza ao pickup
- [ ] Texto do objetivo ativo (`active_objective()`) visível
- [ ] Indicador `MODO: NATACAO` ou `MODO: GOSMA` quando aplicável

### Menu (`LANTERN-MENU-15`)
- [ ] Item selecionado mais claro que os demais
- [ ] “Jogar aleatório” usa seed diferente de 42
- [ ] “Sair” encerra processo limpo
- [ ] Pausa não processa movimento/tiro

### Água (`LANTERN-WATER-12`)
- [ ] Shallow: movimento ~60% velocidade, breath recupera
- [ ] Deep: câmera baixa (`y ≈ 0.9`), breath drena, natação ativa
- [ ] Breath zero → vida cai
- [ ] Não atravessa deep sem swimming

### Gosma / slime (`LANTERN-SLIME-11`)
- [ ] Overlay fullscreen verde decai após sair da gosma
- [ ] Partículas ao matar inseto ou dano por contato
- [ ] Velocidade reduzida com `slime_slow`

### Checkpoint (`LANTERN-CHK-16`)
- [ ] Só ativa dentro de ~1.2 m do altar
- [ ] Objetivo “Ative um altar” completa após E
- [ ] Após morte, restore mantém comida/insetos contados salvos

---

## CI

O workflow `.github/workflows/ci.yml` (repositório raiz) executa `ctest -C Release` no job Windows quando configurado para este projeto.

Requisitos locais para checklist manual: GPU OpenGL 2.0+, saída de áudio, assets gerados (`python tools/generate_assets.py`).

---

## Como depurar falhas

| Teste | Falha típica | Ação |
|-------|--------------|------|
| test_procgen | floors baixo | Mais salas ou menos padding em `overlaps` |
| test_procgen | water_count | Chamar `carve_water_pool` no fim de `generate_dungeon` |
| test_collision | posição atravessa | Segundo pass em `move_with_collision` |
| test_objectives | escape cedo | `on_escape_ready` só quando `all_complete()` prévio |
| test_checkpoint | health errado | Copiar todos os campos em `checkpoint_save` |
