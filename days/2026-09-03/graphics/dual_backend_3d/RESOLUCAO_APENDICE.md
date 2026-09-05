# Resolução guiada — apêndice (graphics)


```cpp
glEnable(GL_DEPTH_TEST);
```

adicione:

```cpp
glEnable(GL_CULL_FACE);
glCullFace(GL_BACK);
glFrontFace(GL_CCW);
```

Aqui não é necessário carregar essas três funções com `wglGetProcAddress`: elas pertencem à API OpenGL 1.1 exportada por `opengl32.dll` no Windows e já são declaradas pelo header usado pelo projeto.

---

# Parte F — câmera WASD + mouse sem quebrar o timestep fixo

## 10. TODO `GFX-CAMERA-01`: `camera_forward`

Abra:

```text
starter/common/engine.cpp
```

Localize:

```cpp
Vec3 camera_forward(const CameraState& camera)
```

Substitua por:

```cpp
const float cos_pitch = std::cos(camera.pitch);
return normalize({
    cos_pitch * std::sin(camera.yaw),
    std::sin(camera.pitch),
    -cos_pitch * std::cos(camera.yaw),
});
```

Com `yaw=0` e `pitch=0`, o resultado deve ser aproximadamente `(0,0,-1)`.

## 11. TODO `GFX-CAMERA-02`: `camera_right`

Na função seguinte use:

```cpp
constexpr Vec3 kWorldUp{0.0f, 1.0f, 0.0f};
return normalize(cross(camera_forward(camera), kWorldUp));
```

Para a câmera padrão, o resultado deve apontar aproximadamente para `+X`.

## 12. TODO `GFX-CAMERA-03`: `look_at`

Substitua o placeholder de `look_at` por:

```cpp
const Vec3 forward = normalize(target - eye);
const Vec3 right = normalize(cross(forward, world_up));
const Vec3 up = cross(right, forward);

Mat4 result = Mat4::identity();
result.m[0] = right.x;
result.m[4] = right.y;
result.m[8] = right.z;
result.m[12] = -dot(right, eye);

result.m[1] = up.x;
result.m[5] = up.y;
result.m[9] = up.z;
result.m[13] = -dot(up, eye);

result.m[2] = -forward.x;
result.m[6] = -forward.y;
result.m[10] = -forward.z;
result.m[14] = dot(forward, eye);
return result;
```

Agora rode o teste portátil:

```bat
cmake --build build-starter --config Debug
ctest --test-dir build-starter -C Debug --output-on-failure
```

Nesse ponto `test_camera_yaw_changes_forward_direction` e `test_default_camera_matches_original_view` devem passar.

## 13. TODO `GFX-CAMERA-04`: teclado nos dois frontends

Nos dois arquivos:

```text
starter/software_win32/main.cpp
starter/opengl_win32/main.cpp
```

localize:

```cpp
void update_camera_keyboard(float frame_dt)
```

Substitua o corpo por:

```cpp
constexpr float kCameraSpeed = 3.0f;
const Vec3 forward = camera_forward(g_camera);
const Vec3 right = camera_right(g_camera);

if ((GetAsyncKeyState('W') & 0x8000) != 0) {
    g_camera.position = g_camera.position + forward * (kCameraSpeed * frame_dt);
}
if ((GetAsyncKeyState('S') & 0x8000) != 0) {
    g_camera.position = g_camera.position - forward * (kCameraSpeed * frame_dt);
}
if ((GetAsyncKeyState('D') & 0x8000) != 0) {
    g_camera.position = g_camera.position + right * (kCameraSpeed * frame_dt);
}
if ((GetAsyncKeyState('A') & 0x8000) != 0) {
    g_camera.position = g_camera.position - right * (kCameraSpeed * frame_dt);
}
```

Observe no loop principal que essa função recebe `delta_time` do frame, enquanto `physics_step` continua recebendo `kFixedTimeStep` dentro do acumulador. Não troque um pelo outro.

## 14. TODO `GFX-CAMERA-05`: mouse nos dois frontends

Dentro de `window_proc`, localize `case WM_MOUSEMOVE` e substitua o placeholder por:

```cpp
case WM_MOUSEMOVE: {
    const POINT current{
        static_cast<short>(LOWORD(lparam)),
        static_cast<short>(HIWORD(lparam)),
    };

    if (g_have_last_mouse) {
        constexpr float kMouseSensitivity = 0.004f;
        const float dx = static_cast<float>(current.x - g_last_mouse.x);
        const float dy = static_cast<float>(current.y - g_last_mouse.y);

        g_camera.yaw += dx * kMouseSensitivity;
        g_camera.pitch = std::clamp(
            g_camera.pitch - dy * kMouseSensitivity,
            -1.45f,
            1.45f);
    }

    g_last_mouse = current;
    g_have_last_mouse = true;
    return 0;
}
```

O clamp evita chegar exatamente a ±90°, onde `forward` e `world_up` podem ficar quase paralelos e tornar o cálculo de `right` numericamente ruim.

---

# 15. Validação final

## Testes portáteis

```bat
cmake --build build-starter --config Debug
ctest --test-dir build-starter -C Debug --output-on-failure
```

Esperado:

```text
100% tests passed, 0 tests failed out of 1
```

## Software backend

```bat
build-starter\Debug\software_renderer.exe
```

Verifique:

- triângulos preenchidos;
- depth test;
- Lambert;
- faces traseiras não desenhadas;
- W/S/A/D movem a câmera;
- mouse altera yaw/pitch;
- P pausa a física;
- R restaura cena e câmera.

## OpenGL backend

```bat
build-starter\Debug\opengl_renderer.exe
```

Faça as mesmas verificações. A cena compartilhada deve continuar equivalente conceitualmente nos dois backends.

## Debugging quando algo falhar

**Tela vazia no software:** breakpoint em `draw_cube`; verifique `visible[]`, `signed_area`, `min_x/max_x`, `w0/w1/w2`.

**Tudo some após culling:** verifique o sinal de `signed_area` e confirme que você copiou `return signed_area > 0.0f` em `screen_triangle_front_facing`.

**Câmera anda invertida:** inspecione `camera_forward(g_camera)` com yaw/pitch zero; deve dar aproximadamente `(0,0,-1)`.

**Mouse vira de ponta-cabeça:** confirme `pitch - dy * sensitivity`, não `+ dy`.

**Física muda ao mover câmera:** confirme que `physics_step` ainda está exclusivamente no `while (accumulator >= kFixedTimeStep)`.

**OpenGL shader falha:** use o log já exibido por `compile_shader`; não altere o loader antes de ler o erro.

---

# 16. Compare com a solution somente agora

Depois que seus testes passarem, compare:

```text
starter/common/engine.cpp               ↔ solutions/common/engine.cpp
starter/software_win32/main.cpp         ↔ solutions/software_win32/main.cpp
starter/opengl_win32/main.cpp           ↔ solutions/opengl_win32/main.cpp
```

Todos os TODOs listados no início deste documento têm implementação correspondente na `solutions/`.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `GFX-CAMERA-03` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-CAMERA-01` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-CAMERA-02` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-CULL-01` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-LAMBERT-01` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-CAMERA-04` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-CULL-03` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-CAMERA-05` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-RASTER-01` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
- `GFX-CULL-02` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
- `GFX-CAMERA-04` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
- `GFX-CAMERA-05` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
## Relatório de resolução

### O que foi validado

- Todos os TODOs do `starter/` foram implementados na ordem sugerida.
- Testes com marcadores `PEDAGOGY-TEST` passaram na solution.
- O starter continua falhando nos pontos intencionais até o aluno completar cada ID.

### Armadilhas encontradas

- Leia mensagens de `assert` como contrato, não como bug do teste.
- Compare sempre starter vs solution diff por arquivo.
- Documente no benchmark o que *não* foi medido (I/O, rede, GPU, VM).

### Próximo passo sugerido

Repita o módulo sem consultar a resolução, cronometrando apenas a fase de implementação. Depois leia `BENCHMARK_GUIADO.md` e registre suas observações na seção **Resultados observados**.
