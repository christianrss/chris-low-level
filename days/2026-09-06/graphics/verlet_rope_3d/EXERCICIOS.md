# Exercícios — Portal Verlet Physics

## Fácil — GFX-PORTAL-01

Em `starter/src/math.cpp`, implemente `mat4_transform_point` e `mat4_transform_direction`.

**Aceite:** `mat4_translate({0,0,10})` leva `(0,0,2)` → `(0,0,12)`; direction `(0,0,1)` sob a mesma matriz permanece `(0,0,1)` (sem +10).

Complete `mat4_inverse_rigid` e confira no papel: frame identidade em origem → inversa identidade.

## Médio — GFX-PORTAL-02

Desenhe bases de A `(0,0,0,+Z)` e B `(0,0,10,-Z)`. Implemente `make_frame_matrix` + `make_portal_pair` em `starter/src/portal.cpp`.

**Aceite:** `pair.a_to_b` não é identidade; `world_to_a` de A na origem é identidade (float).

## Médio — GFX-PORTAL-03

Implemente `portal_transport_position` / `portal_transport_velocity`.

**Aceite:** `test_portal_transform` imprime `OK portal transform` — `(0,0,2)→(0,0,8)`, round-trip, `vz: 5→-5`.

## Difícil — GFX-PORTAL-04

Implemente `verlet_step` em `starter/src/verlet.cpp` (integração + `constraint_iters`× `constrain_segments`).

**Aceite:** `test_verlet_rope` → `OK verlet rope` (comprimento ±0.15, miolo desce, endpoints y=5).

**Extra:** damping `vel *= 0.99` antes de integrar; compare comprimento após 60 steps com/sem damping.

## Desafio — GFX-PORTAL-05

Implemente cruzamento de plano + disco + `try_sphere_teleport`.

**Aceite:** `test_sphere_portal` → `OK sphere portal`; esfera em `(5,0,0.5)` com `portal_radius=1` não teleporta.

**Extra:** se um nó da corda cruzar o portal, transporte `points[i]` e `prev_points[i]` (não coberto pelo teste oficial).

## Desafio — GFX-PORTAL-06 (visual obrigatório)

WGL com `cStencilBits=8`, `render_through_portal` 1 nível, loop Win32 em `main_opengl.cpp`.

**Aceite (Caso manual):** `portal_demo.exe` — ver sala através dos portais; esfera reaparece do outro lado. Sem stencil, o exercício **não** está completo.
