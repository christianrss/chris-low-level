# Teoria passo a passo — Chris OS graphics reference

## 1. Por que user-space primeiro?
Antes de escrever um compositor dentro do seu SO, é útil ter uma implementação portátil que funcione como oráculo. Se o backend de framebuffer produzir pixels diferentes, você tem uma referência determinística.

## 2. Surface
Uma surface é largura, altura e pixels RGBA. O índice row-major é `y*width+x`.

## 3. Clipping
Desenhar um retângulo parcialmente fora da tela não deve acessar memória inválida. Primeiro intersectamos o retângulo com `[0,width)x[0,height)`.

## 4. Alpha over
Para alpha de 0..255: `out = (src*alpha + dst*(255-alpha))/255`. A versão de hoje mantém output alpha opaco para simplificar.

## 5. Window/compositor roadmap
Futuro: shared surfaces, damage tracking, input focus, z-order, frame pacing, cursor, window protocol, GUI toolkit e backend virtio-gpu.

## 6. Exercícios
**Fácil:** calcule índice de pixel.  
**Médio:** implemente `fill_rect` com clipping.  
**Difícil:** implemente alpha-over e z-order.  
**Desafio:** adicione damage rectangles e meça quanto trabalho é evitado quando só 5% da tela muda.
