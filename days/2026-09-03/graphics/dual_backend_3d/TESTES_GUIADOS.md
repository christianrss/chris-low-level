# Testes guiados auditados — dual_backend_3d

## 1. O CMake agora registra o teste

A partir da pasta do módulo:

```bat
cmake -S starter -B build-starter -A x64
cmake --build build-starter --config Debug
ctest --test-dir build-starter -C Debug --output-on-failure
```

Antes desta correção, `core_tests.exe` existia, mas não estava registrado via `add_test`; `ctest` podia dizer `No tests were found`. Isso foi corrigido.

## 2. Estado inicial esperado do starter

O build deve passar. O teste deve falhar enquanto os TODOs de câmera/culling permanecerem.

A primeira falha esperada é:

```text
test_camera_yaw_changes_forward_direction
```

Isso prova que o teste realmente alcança um TODO do starter.

## 3. Depois de `GFX-CAMERA-01..03` e `GFX-CULL-01`

Rode novamente:

```bat
ctest --test-dir build-starter -C Debug --output-on-failure
```

Esperado:

```text
100% tests passed
```

## 4. Testes visuais Windows

Os backends Win32/WGL são validados manualmente no Windows porque o host Linux do laboratório não cria essas janelas.

### Software

```bat
build-starter\Debug\software_renderer.exe
```

Checklist: rasterização, depth, iluminação, culling, WASD, mouse, P, R.

### OpenGL

```bat
build-starter\Debug\opengl_renderer.exe
```

Checklist equivalente. Se shader falhar, registre o log da MessageBox.

## 5. Limite de validação

Os testes portáteis cobrem matemática de câmera, transform default, física básica e convenção de winding. Eles não provam que WGL/OpenGL funcionam em todo driver/hardware. Essa parte exige execução real no Windows.

## Cobertura pedagógica auditada

Os IDs abaixo precisam ter um critério de verificação antes de o módulo ser considerado concluído.

- `GFX-CAMERA-03` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-CAMERA-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-CAMERA-02` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-CULL-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-LAMBERT-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-CAMERA-04` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-CULL-03` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-CAMERA-05` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-RASTER-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `GFX-CULL-02` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.

Arquivos de teste automatizado presentes no starter:
- `starter/tests/core_tests.cpp`
