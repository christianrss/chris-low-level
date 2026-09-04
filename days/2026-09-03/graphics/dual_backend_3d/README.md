# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/` e localize os TODOs.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Compile/teste após cada etapa.
5. Só então compare com `solutions/`.

---

# Low-Level 3D em tempo real: software renderer vs OpenGL

A mesma cena roda em dois backends para comparar exatamente o que muda quando uma API grafica assume parte do pipeline de renderizacao.

- `solutions/software_win32/`: rasterizador 3D escrito na CPU. Win32 serve apenas para janela, eventos e apresentacao via `StretchDIBits`.
- `solutions/opengl_win32/`: a mesma cena, animacao e fisica, mas os vertices sao enviados para a GPU via OpenGL. O contexto WGL e criado manualmente e as funcoes modernas sao carregadas com `wglGetProcAddress`.
- `starter/`: versao para os exercicios. Ela continua compilavel, mas deixa TODOs no rasterizador CPU e no fragment shader.
- `docs/COMPARISON.md`: comparacao etapa a etapa entre os dois pipelines.

## Correcao para Visual Studio 18 / MSVC

Esta revisao corrige a colisao historica entre `windows.h` e `std::min` / `std::max`.

O Win32 SDK pode definir macros `min` e `max`. O projeto agora define `NOMINMAX` antes de incluir
`windows.h` e tambem adiciona `NOMINMAX` via CMake para os dois executaveis Win32.

Tambem foram feitas duas melhorias:

1. o codigo foi reformatado para manter indentacao, quebras de linha e comentarios didaticos;
2. `WM_SIZE` no backend OpenGL nao chama mais `glViewport` antes da criacao do contexto WGL.

## Build recomendado no Windows

Abra um terminal em que `cmake` esteja disponivel e execute a partir da raiz do laboratorio.

### Solucao completa

```bat
rmdir /s /q build-solution 2>nul
cmake -S solutions -B build-solution -A x64
cmake --build build-solution --config Release
```

Omitir `-G` deixa o CMake selecionar automaticamente o Visual Studio instalado. Se voce quiser
selecionar explicitamente o Visual Studio 2026 e sua versao do CMake oferecer esse generator:

```bat
cmake -S solutions -B build-solution -G "Visual Studio 18 2026" -A x64
cmake --build build-solution --config Release
```

Para ver os generators reconhecidos pela sua instalacao local:

```bat
cmake --help
```

### Starter

```bat
rmdir /s /q build-starter 2>nul
cmake -S starter -B build-starter -A x64
cmake --build build-starter --config Release
```

## Executaveis esperados

```text
build-solution\Release\software_renderer.exe
build-solution\Release\opengl_renderer.exe
build-solution\Release\core_tests.exe
```

Execute primeiro:

```bat
build-solution\Release\core_tests.exe
```

Depois abra separadamente os dois renderers.

## Controles

- `P`: pausa ou continua a simulacao.
- `R`: reinicia a simulacao.
- `Esc`: fecha a janela.

## Cena compartilhada

`common/engine.cpp` implementa a parte compartilhada pelos dois backends:

- `Vec3`, `Vec4` e `Mat4`;
- projection e view matrices;
- fixed-step physics a 120 Hz;
- gravidade, colisao com plano e restitution;
- animacao hierarquica de um braco com duas articulacoes;
- lista compartilhada de `DrawItem`.

Os dois renderers recebem os mesmos transforms. A diferenca principal e o caminho dos triangulos ate os pixels.

## Por que a versao software ainda usa Win32?

Um programa comum em user-space precisa do sistema operacional para criar uma janela e apresentar
pixels ao desktop. O que foi implementado manualmente e o pipeline 3D: transformacoes, projecao,
rasterizacao, coordenadas baricentricas, depth test, iluminacao e framebuffer.

A trilha de drivers/kernel pode, mais adiante, descer outra camada e estudar framebuffer de
hardware, WDDM, device drivers e interfaces de GPU em laboratorio apropriado.
