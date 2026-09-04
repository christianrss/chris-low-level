# Testes guiados - 3D, animação e física

## Teste 1 - matriz identidade

Multiplicar qualquer vetor por `Mat4::identity()` deve preservar todos os componentes.

## Teste 2 - tradução

Aplique `translate(2,3,4)` ao ponto `(1,1,1,1)`. O resultado deve ser aproximadamente `(3,4,5,1)`.

## Teste 3 - gravidade altera velocidade

Depois de `physics_step(scene, dt)`, com corpo no ar, `velocity.y` deve diminuir aproximadamente `9.81*dt`.

## Teste 4 - piso não pode ser atravessado

Inicialize o corpo quase abaixo do piso e com velocidade negativa. Após o passo, a base do corpo deve estar no piso ou acima dele e a velocidade vertical deve ter mudado de sinal pela restituição.

## Teste 5 - hierarquia de animação

Mude o tempo da cena. `build_draw_list()` deve produzir o mesmo número de objetos, mas as matrizes do braço devem mudar. Isso testa que a animação está realmente ligada ao tempo.

## Comparação de backends

Os testes unitários devem atingir o `scene_core`, que é compartilhado. A validação visual dos backends usa a mesma cena: se software e OpenGL divergirem, compare transformações, culling, depth convention e viewport antes de culpar a física.
