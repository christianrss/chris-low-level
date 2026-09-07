# Teoria passo a passo — Portal Verlet Physics

## 1. O que estamos construindo

Um mini-engine 3D educacional: **Mat4 column-major**, **par de portais A↔B**, **corda Verlet**, **esfera que teleporta**, e **demo OpenGL WGL** com **stencil de 1 nível** (`portal_demo.exe`).

TODOs: `GFX-PORTAL-01` … `GFX-PORTAL-06`. Testes CPU em `starter/tests/`; o efeito visual de portal **não é opcional** — é o Caso manual 6.

## 2. Por que Mat4 + portal + Verlet juntos

O transporte portal é composição de bases rígidas. Verlet força constraints sem solver linear. A demo amarra os dois: a matemática dos testes CPU vira pixels no stencil. Sem a demo, o aluno “passa” nos asserts e nunca vê a recursão de 1 nível.

## 3. Mat4 column-major (`GFX-PORTAL-01`)

### O quê
`Mat4` em `math.hpp` guarda 16 floats em **column-major** (OpenGL): índice `m[col*4 + row]`. APIs: `mat4_identity`, `mat4_translate`, `mat4_multiply`, `mat4_inverse_rigid`, `mat4_transform_point`, `mat4_transform_direction`.

### Como

```text
| m0  m4  m8  m12 |   | x |
| m1  m5  m9  m13 | × | y |
| m2  m6  m10 m14 |   | z |
| m3  m7  m11 m15 |   | 1 |   (ponto)

direção: mesma rotação, sem m12/m13/m14
```

Inversa rígida: transpor os 3×3 das colunas `right/up/forward` e `t' = (-dot(right,pos), -dot(up,pos), -dot(forward,pos))`.

### Por quê
GLSL/`glLoadMatrixf` esperam column-major. Confundir com row-major espelha eixos sem warning do compilador.

### Trace numérico — translate + ponto

```text
T = mat4_translate({0,0,10})
p = (0,0,2)
z' = 0·x + 0·y + 1·z + 10 = 12
→ (0,0,12)   [Caso 1 de test_portal_transform]
```

### Trace numérico — identity

```text
I · (1,2,3) = (1,2,3)
```

### Invariantes
- `mat4_multiply(I, M) == M`
- `transform_point` inclui translação; `transform_direction` não
- `inverse_rigid` só é válida para rotação ortonormal + translação (sem escala não uniforme)

### Bugs comuns
| Sintoma | Causa |
|---------|-------|
| eixo espelhado | misturou row/column no índice |
| velocity “salta” de origem | usou `transform_point` em velocidade |
| inverse errada | esqueceu o sinal nos dots da translação |

---

## 4. Frame de portal (`GFX-PORTAL-02`)

### O quê
`PortalFrame { position, forward, up }`. `make_frame_matrix` monta a Mat4 do portal. `make_portal_pair` preenche `world_to_a`, `world_to_b`, `a_to_b`, `b_to_a`.

### Como

```text
f = normalize(forward)
r = normalize(cross(f, up))
u = normalize(cross(r, f))

colunas da Mat4: [ r | u | f | position ]
```

```text
a_to_b = frame_b × inverse_rigid(frame_a)
b_to_a = frame_a × inverse_rigid(frame_b)
```

(`portal_link_matrix` em `solutions/src/portal.cpp`.)

### Por quê
Coordenadas locais do portal A devem mapear 1:1 para locais de B. Sem base ortonormal, o “chão” do outro lado inclina ou escala.

### Trace numérico — bases face a face

```text
A: pos=(0,0,0), forward=+Z, up=+Y
  r=(1,0,0), u=(0,1,0), f=(0,0,1)

B: pos=(0,0,10), forward=-Z, up=+Y
  f=(0,0,-1)
  r = cross(f,up) = (1,0,0)
  u = cross(r,f) = (0,1,0)
```

Ponto mundo no eixo de A a 2 unidades “para frente” do plano: `(0,0,2)`.

### Invariantes
- `forward` ⟂̸ `up` (senão `r` degenera)
- det da rotação ≈ +1 (mão direita)

### Bugs comuns
- `up` paralelo a `forward`
- esquecer `normalize` após cross
- guardar `a_to_b` como `frame_a × inv(frame_b)` (ordem invertida)

---

## 5. Transporte A↔B (`GFX-PORTAL-03`)

### O quê
`portal_transport_position(pair, from_a, world_pos)` e `portal_transport_velocity(..., world_vel)`.

### Como

```text
link = from_a ? pair.a_to_b : pair.b_to_a
posição  = mat4_transform_point(link, world_pos)
velocidade = mat4_transform_direction(link, world_vel)
```

### Por quê
Uma única Mat4 cobre portais rotacionados; evita `if` por eixo. Velocidade sem translação preserva momentum relativo ao frame.

### Trace numérico — posição (Caso 3 dos testes)

```text
A em z=0 face +Z; B em z=10 face -Z
inv(frame_a) = I  (origem + eixos canônicos)
a_to_b = frame_b
(0,0,2) → pos_B + 2·f_B = (0,0,10) + 2·(0,0,-1) = (0,0,8)
```

### Trace numérico — velocidade

```text
v_in = (0,0,5)
v_out = mat4_transform_direction(a_to_b, v_in) = (0,0,-5)
```

Round-trip: A→B→A restaura `(0,0,2)`.

### Invariantes
- Round-trip posição (float ≈)
- Componente ao longo do normal inverte para o par face-a-face deste lab

### Bugs comuns
| Sintoma | Causa |
|---------|-------|
| z=12 em vez de 8 | flip Z extra além da composição |
| round-trip falha | `b_to_a` não é o inverso de `a_to_b` |
| esfera “cola” | velocity via `transform_point` |

---

## 6. Verlet rope (`GFX-PORTAL-04`)

### O quê
`VerletRope { points, prev_points, segment_length }`. `verlet_init_rope` amostra a reta; `verlet_step` integra + constraints; endpoints 0 e n−1 fixos.

### Como

```text
para i = 1 .. n-2:
  vel = points[i] - prev_points[i]
  next = points[i] + vel + gravity * dt²
  prev_points[i] = points[i]
  points[i] = next

repetir constraint_iters:
  para cada segmento (i,i+1):
    puxar/empurrar para dist == segment_length
    (não mover i==0 nem i==n-1)
```

### Por quê
Verlet embute velocidade na diferença de posição — estável com constraints iterativas (Jakobsen). Euler explícito + spring stiff explode com o mesmo `dt`.

### Trace numérico — um passo no miolo

```text
ponto i: pos=(2,5,0), prev=(2,5,0), g=(0,-9.8,0), dt=1/60
vel = (0,0,0)
a·dt² = (0, -9.8/3600, 0) ≈ (0, -0.00272, 0)
next ≈ (2, 4.99728, 0)
```

Após 60 frames com constraints, `points[2].y < 5` e comprimento total ≈ inicial (±0.15 no teste).

### Invariantes
- `points[0]` e `points.back()` imóveis no step
- `verlet_total_length` estável após iterações suficientes

### Bugs comuns
- não atualizar `prev_points` → corda “congela” ou explode
- mover endpoints no constrain
- `dt` grande demais (use `1/60`)

---

## 7. Esfera e portal (`GFX-PORTAL-05`)

### O quê
`Sphere { center, radius, velocity }`. `sphere_crosses_portal_plane` + `try_sphere_teleport` + `sphere_step` (gravidade/chão).

### Como

```text
dist = dot(center - frame.pos, normalize(forward))
cruza se: dist <= sphere.radius
       e  dist + sphere.radius >= 0
       e  projeção no disco (raio portal_radius) contém o centro

teleporte:
  center = portal_transport_position(...)
  velocity = portal_transport_velocity(...)
```

`inside_portal_disc` usa `inverse_rigid(make_frame_matrix(frame))` e checa `sqrt(local.x²+local.y²) ≤ portal_radius`.

### Por quê
Só distância ao plano teleporta esfera ao lado do portal (fora do quad). Sem transformar velocity, o momentum aponta para o portal de saída e a esfera reentra no mesmo frame.

### Trace numérico — Caso test_sphere_portal

```text
sphere.center=(0,0,-0.2), radius=0.3, vel=(0,0,4)
portal A: pos=0, n=+Z, portal_radius=2

dist = -0.2
dist + radius = 0.1 ≥ 0  e  dist ≤ 0.3  → cruza
dentro do disco (x=y=0) → true

após A→B: center.z ≈ 10.2, velocity.z ≈ -4
```

Esfera em `(5,0,0.5)` com `portal_radius=1` → fora do disco → sem teleporte.

### Invariantes
- Fora do disco: `try_sphere_teleport` retorna `false` sem mutar
- Após teleporte bem-sucedido, centro está no lado destino

### Bugs comuns
- teleportar todo frame sem hysterese (ok neste lab; em jogo precisa cooldown)
- `portal_radius` < offset lateral do centro

---

## 8. Demo OpenGL + stencil 1 nível (`GFX-PORTAL-06`) — visual obrigatório

### O quê
`portal_demo.exe`: WGL (`portal_gl_init`), cena (`PortalScene`), câmera, `portal_gl_render_frame`. Controles: WASD, mouse, Space/clique joga a esfera.

### Como — pipeline de um frame

```text
1. Clear COLOR|DEPTH|STENCIL
2. Draw cena com câmera real (chão, corda, esfera) — sem frames de portal
3. render_through_portal(..., from_a=true):
     a) Color/Depth mask OFF
     b) Stencil ALWAYS → REPLACE 1; desenhar quad do portal A
     c) Color/Depth mask ON; Stencil EQUAL 1
     d) Câmera = mirror_camera_through_portal(..., from_a)
     e) Draw cena (sem frames)
4. Idem para portal B (from_a=false)
5. Desenhar quads coloridos A/B por cima
6. SwapBuffers
```

`PIXELFORMATDESCRIPTOR.cStencilBits = 8` é **obrigatório**. Sem stencil buffer, a máscara não existe e o “portal” vira um quad opaco.

`mirror_camera_through_portal` transporta `eye` e um ponto-alvo 3 unidades à frente; recalcula `yaw`/`pitch`.

### Por quê (visual requerido, não opcional)
CPU tests provam `(0,0,2)→(0,0,8)`. Só a demo prova que a **máscara stencil** restringe a vista espelhada ao interior do portal. Stencil 1 nível = uma recursão: você vê a sala do outro lado, **não** um portal-dentro-de-portal.

### Trace operacional — contador

```text
portal_gl_render_frame zera ctx.stencil_passes
cada render_through_portal faz ++ctx.stencil_passes
→ esperado: 2 por frame (A e B)
```

### Invariantes
- Stencil limpo a cada subpass
- Conteúdo espelhado só onde stencil == 1
- Demo linka `opengl32`/`gdi32`/`user32` (Windows)

### Bugs comuns
| Sintoma | Causa |
|---------|-------|
| tela preta / MessageBox WGL | `cStencilBits=0` ou pixel format sem stencil |
| vê cena inteira espelhada | esqueceu `GL_EQUAL` / não desenhou máscara |
| portal “vazio” | não chamou `mirror_camera_through_portal` |
| esfera não atravessa visualmente | `try_sphere_teleport` ausente no loop de `simulate` |

---

## 9. Diagrama do pipeline

```text
math (Mat4) ──► portal (frames + transport)
                      │
              ┌───────┴────────┐
              ▼                ▼
         verlet_step      sphere_teleport
              │                │
              └───────┬────────┘
                      ▼
              portal_gl_render_frame
                 (stencil 1-level)
                      ▼
               portal_demo.exe
```

## 10. Complexidade

| Operação | Custo |
|----------|-------|
| `portal_transport_*` | O(1) |
| `verlet_step` | O(N · iters) |
| stencil pass | fill-rate do quad + redraw da cena |

## 11. Como saber se está correto

1. `test_portal_transform.exe` → `OK portal transform`
2. `test_verlet_rope.exe` → `OK verlet rope`
3. `test_sphere_portal.exe` → `OK sphere portal`
4. `portal_demo.exe`: olhar pelo azul/laranja e ver a sala; arremessar esfera e vê-la sair do outro portal

## 12. Referências

- Jakobsen — Verlet constraints (GDC)
- Portal rendering clássico (máscara + câmera linkada)
- OpenGL fixed-function stencil (`glStencilFunc` / `glStencilOp`)
