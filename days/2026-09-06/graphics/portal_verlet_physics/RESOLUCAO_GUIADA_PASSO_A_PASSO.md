# RESOLUÇÃO GUIADA — Graphics / Portal Verlet Physics

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `GFX-PORTAL-01` | `starter/src/math.cpp` | `mat4_inverse_rigid`, `mat4_transform_point`, `mat4_transform_direction` |
| `GFX-PORTAL-02` | `starter/src/portal.cpp` | `make_frame_matrix`, `make_portal_pair` |
| `GFX-PORTAL-03` | `starter/src/portal.cpp` | `portal_transport_position`, `portal_transport_velocity` |
| `GFX-PORTAL-04` | `starter/src/verlet.cpp` | `verlet_step` |
| `GFX-PORTAL-05` | `starter/src/sphere_portal.cpp` | `sphere_crosses_portal_plane`, `try_sphere_teleport` |
| `GFX-PORTAL-06` | `starter/src/render_gl.cpp`, `starter/src/main_opengl.cpp` | WGL + stencil + loop |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` em `solutions/src/`, e `PEDAGOGY-TEST: ID` nos testes / `main_opengl.cpp`.

> Trabalhe em `days/2026-09-06/graphics/portal_verlet_physics/starter/`. `solutions/` é gabarito — só depois da tentativa.

> Continuação (`GFX-PORTAL-05` e `GFX-PORTAL-06`): `RESOLUCAO_APENDICE.md`.

---

## 0. Baseline (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\graphics\portal_verlet_physics\starter
cmake -S . -B build -A x64
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Stubs: `transform_point` devolve `p` sem translação; `portal_transport_*` devolve o input; `verlet_step` só chama constraint; esfera nunca teleporta. Asserts falham — intencional.

---

## GFX-PORTAL-01 — Mat4 rígida e transforms

### 1. O problema

Em `starter/src/math.cpp`:

```cpp
Mat4 mat4_inverse_rigid(const Mat4& m) {
    // TODO [GFX-PORTAL-01]
    (void)m;
    return mat4_identity();
}

Vec3 mat4_transform_point(const Mat4& m, Vec3 p) {
    // TODO [GFX-PORTAL-01]
    (void)m;
    return p;
}

Vec3 mat4_transform_direction(const Mat4& m, Vec3 d) {
    // TODO [GFX-PORTAL-01]
    (void)m;
    return d;
}
```

Com identity falsa e ponto sem translação, `mat4_translate({0,0,10}) · (0,0,2)` não chega a z=12.

### 2. O algoritmo

```text
inverse_rigid(M):
  right=(m0,m1,m2), up=(m4,m5,m6), forward=(m8,m9,m10), pos=(m12,m13,m14)
  R^T nas colunas → linhas de right/up/forward
  t' = (-dot(right,pos), -dot(up,pos), -dot(forward,pos))

transform_point:  p' = R·p + t
transform_direction: d' = R·d
```

### 3. Código

Substitua os três corpos em `starter/src/math.cpp` (APIs de `math.hpp`):

```cpp
Mat4 mat4_inverse_rigid(const Mat4& m) {
    Vec3 right = {m.m[0], m.m[1], m.m[2]};
    Vec3 up = {m.m[4], m.m[5], m.m[6]};
    Vec3 forward = {m.m[8], m.m[9], m.m[10]};
    Vec3 pos = {m.m[12], m.m[13], m.m[14]};

    Mat4 inv = mat4_identity();
    inv.m[0] = right.x;  inv.m[1] = up.x;  inv.m[2] = forward.x;
    inv.m[4] = right.y;  inv.m[5] = up.y;  inv.m[6] = forward.y;
    inv.m[8] = right.z;  inv.m[9] = up.z;  inv.m[10] = forward.z;
    inv.m[12] = -vec3_dot(right, pos);
    inv.m[13] = -vec3_dot(up, pos);
    inv.m[14] = -vec3_dot(forward, pos);
    return inv;
}

Vec3 mat4_transform_point(const Mat4& m, Vec3 p) {
    float x = m.m[0] * p.x + m.m[4] * p.y + m.m[8] * p.z + m.m[12];
    float y = m.m[1] * p.x + m.m[5] * p.y + m.m[9] * p.z + m.m[13];
    float z = m.m[2] * p.x + m.m[6] * p.y + m.m[10] * p.z + m.m[14];
    return {x, y, z};
}

Vec3 mat4_transform_direction(const Mat4& m, Vec3 d) {
    float x = m.m[0] * d.x + m.m[4] * d.y + m.m[8] * d.z;
    float y = m.m[1] * d.x + m.m[5] * d.y + m.m[9] * d.z;
    float z = m.m[2] * d.x + m.m[6] * d.y + m.m[10] * d.z;
    return {x, y, z};
}
```

### 4. Entenda

- Colunas 0/1/2 = eixos do frame; coluna 3 = origem.
- Transposta no 3×3 = inversa da rotação ortonormal.
- `transform_point` usa `m12..m14`; direction não — senão velocidade herda origem do portal.

### 5. Verificação

```powershell
cmake --build build --config Release
.\build\Release\test_portal_transform.exe
```

Ainda **FAIL** no assert `through.z == 8` (faltam 02/03). Passa o trecho Mat4: identity e translate z=12 se você instrumentar cedo; o binário oficial falha no portal.

---

## GFX-PORTAL-02 — Frame e `PortalPair`

### 1. O problema

```cpp
Mat4 make_frame_matrix(const PortalFrame& frame) {
    // TODO [GFX-PORTAL-02]
    (void)frame;
    return mat4_identity();
}

PortalPair make_portal_pair(PortalFrame a, PortalFrame b) {
    // TODO [GFX-PORTAL-02]
    PortalPair pair{};
    pair.portal_a = a;
    pair.portal_b = b;
    return pair;
}
```

Sem `a_to_b` preenchido, transporte não tem link.

### 2. O algoritmo

```text
f,r,u ortonormais (cross + normalize)
Mat4 colunas [r|u|f|pos]
world_to_a = inverse_rigid(frame_a)
a_to_b = frame_b × inverse_rigid(frame_a)
b_to_a = frame_a × inverse_rigid(frame_b)
```

### 3. Código

Em `starter/src/portal.cpp`:

```cpp
Mat4 make_frame_matrix(const PortalFrame& frame) {
    Vec3 f = vec3_normalize(frame.forward);
    Vec3 r = vec3_normalize({f.y * frame.up.z - f.z * frame.up.y,
                             f.z * frame.up.x - f.x * frame.up.z,
                             f.x * frame.up.y - f.y * frame.up.x});
    Vec3 u = vec3_normalize({r.y * f.z - r.z * f.y,
                             r.z * f.x - r.x * f.z,
                             r.x * f.y - r.y * f.x});

    Mat4 m = mat4_identity();
    m.m[0] = r.x; m.m[1] = r.y; m.m[2] = r.z;
    m.m[4] = u.x; m.m[5] = u.y; m.m[6] = u.z;
    m.m[8] = f.x; m.m[9] = f.y; m.m[10] = f.z;
    m.m[12] = frame.position.x;
    m.m[13] = frame.position.y;
    m.m[14] = frame.position.z;
    return m;
}

static Mat4 portal_link_matrix(const Mat4& a, const Mat4& b) {
    return mat4_multiply(b, mat4_inverse_rigid(a));
}

PortalPair make_portal_pair(PortalFrame a, PortalFrame b) {
    PortalPair pair{};
    pair.portal_a = a;
    pair.portal_b = b;
    Mat4 frame_a = make_frame_matrix(a);
    Mat4 frame_b = make_frame_matrix(b);
    pair.world_to_a = mat4_inverse_rigid(frame_a);
    pair.world_to_b = mat4_inverse_rigid(frame_b);
    pair.a_to_b = portal_link_matrix(frame_a, frame_b);
    pair.b_to_a = portal_link_matrix(frame_b, frame_a);
    return pair;
}
```

### 4. Entenda

- `cross(f, up)` → right; `cross(r, f)` → up reortogonalizado.
- `mat4_multiply(b, inv(a))`: ponto em mundo → espaço A → apply frame B.
- `world_to_*` fica disponível para disco local da esfera (05).

### 5. Verificação

Rebuild. Transporte ainda stub → assert de z=8 continua falhando. Confira no debugger que `pair.a_to_b.m[14]` (translação z do link) não é zero.

---

## GFX-PORTAL-03 — Transporte posição/velocidade

### 1. O problema

```cpp
Vec3 portal_transport_position(...) {
    // TODO [GFX-PORTAL-03]
    return world_pos;
}
Vec3 portal_transport_velocity(...) {
    // TODO [GFX-PORTAL-03]
    return world_vel;
}
```

### 2. O algoritmo

```text
link = from_a ? a_to_b : b_to_a
pos' = transform_point(link, pos)
vel' = transform_direction(link, vel)
```

### 3. Código

```cpp
Vec3 portal_transport_position(const PortalPair& pair, bool from_a, Vec3 world_pos) {
    const Mat4& link = from_a ? pair.a_to_b : pair.b_to_a;
    return mat4_transform_point(link, world_pos);
}

Vec3 portal_transport_velocity(const PortalPair& pair, bool from_a, Vec3 world_vel) {
    const Mat4& link = from_a ? pair.a_to_b : pair.b_to_a;
    return mat4_transform_direction(link, world_vel);
}
```

### 4. Entenda

- Mesmo `link` para pos e vel; só muda o tipo de transform.
- Trace: `(0,0,2)` → `(0,0,8)`; `(0,0,5)` → `(0,0,-5)`; round-trip restaura.

### 5. Verificação

```powershell
cmake --build build --config Release
.\build\Release\test_portal_transform.exe
```

Esperado:

```text
OK portal transform
```

---

## GFX-PORTAL-04 — `verlet_step`

### 1. O problema

```cpp
void verlet_step(VerletRope& rope, Vec3 gravity, float dt, int constraint_iters) {
    // TODO [GFX-PORTAL-04]
    (void)gravity;
    (void)dt;
    (void)constraint_iters;
    constrain_segments(rope);
}
```

Só constraint sem integração: miolo não cai → `points[2].y < mid_before.y` falha.

### 2. O algoritmo

```text
para i=1..n-2:
  vel = points[i]-prev[i]
  next = points[i] + vel + g*dt*dt
  prev[i]=points[i]; points[i]=next
para k=0..constraint_iters-1:
  constrain_segments(rope)   // já no arquivo
```

### 3. Código

```cpp
void verlet_step(VerletRope& rope, Vec3 gravity, float dt, int constraint_iters) {
    const size_t n = rope.points.size();
    if (n < 2) return;

    for (size_t i = 1; i + 1 < n; ++i) {
        Vec3 current = rope.points[i];
        Vec3 velocity = vec3_sub(current, rope.prev_points[i]);
        Vec3 next = vec3_add(vec3_add(current, velocity), vec3_scale(gravity, dt * dt));
        rope.prev_points[i] = current;
        rope.points[i] = next;
    }

    for (int k = 0; k < constraint_iters; ++k) {
        constrain_segments(rope);
    }
}
```

### 4. Entenda

- `i=1 .. n-2` preserva endpoints (init já copiou start/end).
- `dt*dt` multiplica aceleração (forma clássica Verlet).
- `constrain_segments` já evita mover índice 0 e n−1.

### 5. Verificação

```powershell
.\build\Release\test_verlet_rope.exe
```

```text
OK verlet rope
```

---

## Próximos TODOs

`GFX-PORTAL-05` (esfera) e `GFX-PORTAL-06` (demo stencil) estão em **`RESOLUCAO_APENDICE.md`**.

Gabarito CPU completo:

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\graphics\portal_verlet_physics\solutions
cmake -S . -B build -A x64
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Demo visual (obrigatória):

```powershell
cmake -S . -B build-demo -A x64 -DPORTAL_OPENGL=ON
cmake --build build-demo --config Release
.\build-demo\Release\portal_demo.exe
```

---

## Relatório de resolução

### O que foi validado

- TODOs `GFX-PORTAL-01..04` em `starter/src/{math,portal,verlet}.cpp`.
- `test_portal_transform` / `test_verlet_rope` imprimem `OK …`.
- Continuação 05–06 e checklist visual: ver apêndice.

### Armadilhas

- `transform_point` em velocity → teleporte com offset fantasma.
- Ordem `mat4_multiply(b, inv(a))` invertida → z=12 em vez de 8.
- Verlet sem atualizar `prev_points` → sem queda.

### Depuração e saída esperada

- Trace manual `(0,0,2)→(0,0,8)` antes de OpenGL.
- CPU: três `OK` nos testes; visual: Caso manual 6 no apêndice / `TESTES_GUIADOS.md`.

### Próximo passo

Implementar 05–06 pelo apêndice; preencher checklist do relatório lá; medir FPS em `BENCHMARK_GUIADO.md`.


### Por que funciona?

Cada passo acima preserva o contrato do header/API e o invariante de round-trip; veja o algoritmo na seção correspondente.
