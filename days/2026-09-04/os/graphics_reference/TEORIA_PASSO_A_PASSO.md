# Teoria passo a passo — Surface e compositor 2D

## 1. Surface
Uma surface é uma matriz de pixels RGBA em memória. Nosso layout é row-major: índice `y*width+x`.

## 2. Clipping
Desenhar fora do buffer corromperia memória num kernel real. `fill_rect` recorta o retângulo nos limites da surface.

## 3. Layers
Uma layer referencia uma surface e uma posição `(x,y)` no destino. Ordem do vetor define z-order simples: layers posteriores são compostas por cima.

## 4. Alpha source-over
Usamos uma aproximação inteira para RGB, assumindo destino opaco:

```text
out = src*alpha + dst*(1-alpha)
```

com alpha 0..255. Ainda não tratamos gamma correta, premultiplied alpha nem saída semi-transparente.

## 5. Caminho até o SO
CPU reference → framebuffer abstraction → window server → compositor → virtio-gpu/display driver → damage tracking/vsync/fences.
