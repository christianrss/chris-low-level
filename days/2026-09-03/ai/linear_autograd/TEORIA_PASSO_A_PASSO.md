# IA low-level - neurônio linear, gradientes, SGD e autograd

## O que você precisa entender antes de começar

Treinar um modelo significa ajustar parâmetros para reduzir um erro mensurável. Hoje não usamos NumPy, PyTorch ou TensorFlow para que cada operação fique visível.

### Modelo linear

O modelo mais simples do laboratório é:

```text
prediction = weight * x + bias
```

- `x`: entrada;
- `weight`: peso treinável;
- `bias`: deslocamento treinável;
- `prediction`: saída do modelo;
- `y`: resposta desejada.

### Loss

Usaremos erro quadrático:

```text
error = prediction - y
loss = error * error
```

A loss é um único número. Treinar significa encontrar parâmetros que tornem esse número pequeno.

### Derivada

Uma derivada mede a sensibilidade da saída a uma pequena mudança na entrada. Para `loss = (w*x+b-y)^2`:

```text
dL/dw = 2 * (prediction - y) * x
dL/db = 2 * (prediction - y)
```

O sinal do gradiente indica para que lado a loss aumenta. O gradient descent move o parâmetro na direção oposta:

```text
parameter = parameter - learning_rate * gradient
```

### Batch e média

No dataset há várias amostras. Somamos os gradientes e dividimos pela quantidade de amostras para otimizar a loss média.

### Memória em C

`double xs[]` é uma região contígua. Cada `double` normalmente usa 8 bytes. O índice `xs[i]` é traduzido para um endereço baseado no início do array e no tamanho do elemento. Essa visão será importante quando criarmos tensores, strides, GEMM e kernels SIMD.

### Grafo computacional e autograd

Autograd guarda a história das operações. Cada `Value` conhece os nós que o produziram e uma função local de backward.

```text
w ----*----+
      x    +---- prediction ----(- target)---- square ---- loss
x ---------+              b ----+
```

No backward, começamos com `dL/dL = 1` e percorremos o grafo na ordem inversa. Uma ordenação topológica garante que um nó receba as contribuições dos filhos antes de propagar seu gradiente.

## Passo a passo guiado

1. Calcule manualmente `x=2, w=3, b=1, y=10`.
2. Calcule `prediction`, `error` e `loss`.
3. Derive `dL/dw` e `dL/db`.
4. Aplique um passo de SGD com `lr=0.01`.
5. Abra `starter/python/linear_train.py` e complete o loop.
6. Repita a mesma lógica em C.
7. Observe a diferença entre objetos Python e arrays escalares C.
8. Corrija `starter/python/debug_bug.py` sem olhar o gabarito.
9. Complete `starter/python/autograd_scalar.py` e use a solução apenas para conferir.
10. Compare os gradientes do autograd com os valores calculados em papel.

## Exercícios

- Fácil: forward/loss manual.
- Médio: treinar `y=2x+1` em Python e C.
- Difícil: encontrar o backward incorreto.
- Desafio principal: autograd escalar para `+`, `*`, subtração e quadrado.

## Como saber se está correto

Após 1000 épocas, a referência C chega aproximadamente a:

```text
w=2.004861 b=0.985708 mse=0.000034114
```

O autograd da expressão do exercício deve produzir `dL/dw=-12` e `dL/db=-6`.
