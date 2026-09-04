# Gráficos 3D + animação + física - software renderer vs OpenGL

## O que você precisa entender antes de começar

Este laboratório renderiza a mesma cena de duas maneiras para mostrar o que uma API gráfica abstrai.

### Pixel e framebuffer

Um pixel é uma amostra de cor na tela. Um framebuffer é uma região de memória que guarda as cores dos pixels de um frame. No backend software, o programa mantém esse buffer na RAM e o Win32 apenas apresenta a imagem na janela com `StretchDIBits`.

### Por que ainda existe Win32 na versão “do zero”?

Um programa user-space comum precisa pedir ao sistema operacional uma janela e acesso ao desktop. “Do zero” aqui significa que o pipeline 3D é nosso: transformações, projeção, rasterização, barycentrics, depth test e shading. Criar uma janela sem o sistema operacional exigiria descer para drivers/kernel/framebuffer, que será outra trilha.

### Coordenadas e transformações

Um vértice começa em model/local space. A matriz model coloca o objeto no mundo. A matriz view representa a câmera. A matriz projection aplica perspectiva.

```text
local -> model -> world -> view -> clip -> NDC -> viewport -> pixel
```

Usamos vetores homogêneos `Vec4` porque translação pode ser representada por matriz 4x4.

### Perspective divide

Depois da projeção, dividimos `x`, `y` e `z` por `w`. Isso gera normalized device coordinates. Depois mapeamos `[-1,+1]` para coordenadas da janela.

### Triângulos e barycentrics

A GPU normalmente rasteriza triângulos. No software renderer, calculamos uma bounding box e testamos pixels usando edge functions. Os pesos baricêntricos dizem quanto cada vértice contribui para um ponto interno do triângulo.

### Z-buffer

Sem profundidade, o último triângulo desenhado venceria mesmo estando atrás. O depth buffer guarda o menor/mais próximo valor de profundidade já aceito em cada pixel.

### Lambert

Uma iluminação difusa simples usa o cosseno entre normal e direção da luz:

```text
intensity = max(0, dot(normal, light_direction))
```

No software renderer isso roda na CPU. No OpenGL, um fragment shader executa cálculo equivalente em paralelo na GPU.

### Render loop

Uma aplicação em tempo real repete:

```text
processar eventos -> atualizar física/animação -> renderizar -> apresentar
```

### Physics fixed timestep

A física usa passo fixo de 1/120 s. Isso reduz dependência da taxa de frames. O integrador semi-implícito de Euler faz:

```text
velocity += acceleration * dt
position += velocity * dt
```

### Colisão com plano

Quando a esfera cruza o chão, corrigimos a posição e invertimos a componente vertical da velocidade multiplicando por restitution. É um modelo simples, mas já separa detecção e resposta.

### Animação hierárquica

Um braço possui relações pai-filho. A transformação do cotovelo depende do ombro; a mão depende do cotovelo. Multiplicar transforms acumula essa hierarquia. Mais adiante isso evolui para skeleton, bones, quaternions, keyframes e skinning.

### OpenGL

No backend OpenGL:

1. Win32 cria janela;
2. WGL cria contexto OpenGL;
3. VBO guarda vértices na GPU;
4. vertex shader transforma vértices;
5. rasterizador fixo da GPU encontra fragments;
6. depth test compara profundidade;
7. fragment shader calcula cor;
8. `SwapBuffers` apresenta o frame.

O projeto define `NOMINMAX` antes de `windows.h` para impedir que macros históricas `min` e `max` quebrem `std::min`/`std::max` no MSVC.

## Passo a passo guiado

1. Compile primeiro `core_tests` para validar matemática/física.
2. Rode `software_renderer.exe` e observe a cena.
3. Leia `common/engine.cpp`: essa parte é compartilhada.
4. Leia `software_win32/main.cpp` e acompanhe vértice -> projeção -> triângulo -> pixel.
5. Localize o depth buffer.
6. Rode `opengl_renderer.exe` e compare visualmente.
7. Leia criação do contexto WGL, VBO e shaders.
8. Compare `docs/COMPARISON.md` linha a linha.
9. Complete os TODOs do `starter` somente depois de entender a solução conceitual.
10. Implemente a mesma feature nos dois backends, por exemplo back-face culling, e compare quem faz cada etapa.

## Exercícios

- Fácil: rastrear uma coordenada por model/view/projection e explicar cada espaço.
- Médio: completar rasterização/depth e Lambert nos TODOs do starter.
- Difícil: implementar back-face culling nos dois backends.
- Desafio principal: adicionar câmera controlável e manter física com timestep fixo.

## Como saber se está correto

- `core_tests` deve imprimir `all tests passed`;
- os dois backends devem mostrar a mesma cena lógica;
- pausar/reiniciar deve preservar comportamento compartilhado;
- o software renderer deve continuar funcionando sem chamar OpenGL.
