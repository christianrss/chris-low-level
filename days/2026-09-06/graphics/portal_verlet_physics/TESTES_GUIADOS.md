# Testes guiados — Portal Verlet Physics

## Por que estes casos?

Mat4 errada, link invertido, Verlet sem `prev`, ou teleporte sem disco passam “quase”. Cada caso amarra um `TODO` a um `PEDAGOGY-TEST`. A demo (Caso 6) é **gate visual** — não opcional.

## Caso 1 — Mat4 identity + translate (GFX-PORTAL-01)

**Arquivo:** `starter/tests/test_portal_transform.cpp`

1. `mat4_transform_point(identity, (1,2,3)) == (1,2,3)`.
2. `mat4_translate({0,0,10})` em `(0,0,2)` → z=12.

**Invariante:** point usa translação; identity é ponto fixo.

**Se falhar:** índices column-major em `transform_point` (`m[col*4+row]`).

## Caso 2 — Round-trip portal (GFX-PORTAL-02 + 03)

1. Par A `(0,0,0,+Z)` / B `(0,0,10,-Z)`.
2. `through = transport_position(..., true, (0,0,2))`.
3. `back = transport_position(..., false, through)` ≈ `(0,0,2)`.

**Invariante:** `b_to_a ∘ a_to_b ≈ I` no ponto testado.

## Caso 3 — Offset local z=8 e velocity (GFX-PORTAL-03)

1. `(0,0,2)` → `through.z ≈ 8`.
2. `transport_velocity(..., (0,0,5)).z ≈ -5`.

**Invariante:** face-a-face inverte componente normal; offset 2 unidades preservado no destino.

**Se falhar com z=12:** flip Z extra ou ordem `multiply` invertida.

## Caso 4 — Verlet rope (GFX-PORTAL-04)

**Arquivo:** `starter/tests/test_verlet_rope.cpp`

1. Corda `(0,5,0)→(4,5,0)`, 5 pontos; 60× `verlet_step(g=-9.8, dt=1/60, iters=8)`.
2. `|final_len - initial_len| < 0.15`.
3. Endpoints y=5; `points[2].y` diminuiu.

**Invariante:** endpoints fixos; constraints estabilizam comprimento.

## Caso 5 — Esfera e disco (GFX-PORTAL-05)

**Arquivo:** `starter/tests/test_sphere_portal.cpp`

1. Esfera `(0,0,-0.2)`, r=0.3, v=(0,0,4) cruza A e teleporta → z≈10.2, vz≈−4.
2. Esfera `(5,0,0.5)` com `portal_radius=1` → `try_sphere_teleport` false.

**Invariante:** fora do disco não muta estado.

## Caso 6 — Demo visual / manual (GFX-PORTAL-06) — obrigatório

**Marcador:** `PEDAGOGY-TEST: GFX-PORTAL-06` em `starter/src/main_opengl.cpp` / `solutions/src/main_opengl.cpp`.

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\graphics\portal_verlet_physics\solutions
cmake -S . -B build-demo -A x64 -DPORTAL_OPENGL=ON
cmake --build build-demo --config Release
.\build-demo\Release\portal_demo.exe
```

Checklist:

| # | Observação |
|---|------------|
| 1 | Janela abre (não MessageBox do starter) |
| 2 | Corda + esfera + paredes coloridas |
| 3 | Através do portal azul/laranja vê-se a **sala** (stencil), não só o quad |
| 4 | Space/clique: esfera sai pelo portal oposto |
| 5 | Esc encerra |

Sem item 3, o stencil 1 nível **não** foi implementado — lab incompleto.

## Cobertura pedagógica

| TODO | Casos |
|------|-------|
| GFX-PORTAL-01 | 1 |
| GFX-PORTAL-02 | 2 (frames) |
| GFX-PORTAL-03 | 2–3 |
| GFX-PORTAL-04 | 4 |
| GFX-PORTAL-05 | 5 |
| GFX-PORTAL-06 | 6 (manual) |

## Como depurar

1. Falha z=12 no translate → só 01.
2. Translate ok, portal z≠8 → 02/03.
3. Portal ok, corda não cai → 04 (`prev_points`).
4. Corda ok, esfera não → 05 (disco/dist).
5. CPU ok, portal “opaco” → 06 (`cStencilBits`, `GL_EQUAL`).
