# Teoria passo a passo — neurônio linear, gradientes, SGD e autograd escalar

## 1. O que estamos construindo e por quê

Treinar um modelo significa ajustar parâmetros para reduzir um erro mensurável. Neste módulo não usamos NumPy, PyTorch ou TensorFlow de propósito: cada operação fica visível em Python e em C.

O modelo mais simples é o neurônio linear:

```text
prediction = weight * x + bias
```

- `x`: entrada escalar;
- `weight`, `bias`: parâmetros treináveis;
- `y`: alvo desejado.

A loss quadrática `L = (prediction - y)²` transforma o erro em um único número diferenciável. O gradiente aponta a direção de maior aumento da loss; o SGD anda na direção oposta.

## 2. Como funciona internamente — forward e backward

### Forward

Para cada amostra do batch:

```text
prediction = w*x + b
error      = prediction - y
loss       = error * error
```

### Backward (regra da cadeia manual)

```text
dL/dw = 2 * error * x
dL/db = 2 * error
```

### SGD com média de batch

```text
w := w - lr * (1/N) * Σ dL/dw
b := b - lr * (1/N) * Σ dL/db
```

### Grafo computacional (autograd)

```text
w ----*----+
      x    +---- prediction ----(- target)---- square ---- loss
x ---------+              b ----+
```

Cada nó `Value` guarda pais e uma closure `_backward`. A ordenação topológica garante que filhos propagam gradiente antes dos pais.

## 3. Layout de memória em C

```text
offset | campo   | tamanho
-------|---------|--------
+0     | xs[0]   | 8 bytes (double)
+8     | xs[1]   | 8 bytes
...    | ...     |
```

`xs[i]` é traduzido para `base + i * sizeof(double)`. Essa visão prepara tensores, strides e GEMM.

## 4. Exemplo numérico manual

Dados: `x=2`, `w=3`, `b=1`, `y=10`, `lr=0.01`.

```text
prediction = 3*2 + 1 = 7
error      = 7 - 10 = -3
loss       = 9
dL/dw      = 2*(-3)*2 = -12
dL/db      = 2*(-3)   = -6
w_new      = 3 - 0.01*(-12) = 3.12
b_new      = 1 - 0.01*(-6)  = 1.06
```

O autograd do exercício deve reproduzir `dL/dw=-12` e `dL/db=-6`.

## 5. Invariantes

- Gradientes de um nó com múltiplos filhos somam contribuições (`+=`, nunca `=`).
- `loss.backward()` inicia com `dL/dL = 1`.
- Média do batch deve ser aplicada antes do passo SGD se a loss declarada é MSE média.
- Em C, divisão de gradientes usa `double`; evite divisão inteira acidental.

## 6. Complexidade

- Forward por amostra: O(1).
- Backward por nó do grafo: O(1) por aresta.
- Treino com `E` épocas e `N` amostras: O(E·N).
- Ordenação topológica: O(V + E) no tamanho do grafo (pequeno aqui).

## 7. Bugs comuns

- Trocar `dL/dw` com `dL/db` (esquecer o fator `x`).
- Esquecer de zerar acumuladores `d_weight`/`d_bias` a cada época.
- Usar `=` em vez de `+=` no backward com grafo ramificado.
- Não normalizar pelo batch e depois culpar o learning rate.
- Em C, esquecer cast para `double` na média.

## 8. Comparação com sistemas de produção

| Aspecto | Este laboratório | PyTorch / JAX |
|---------|------------------|---------------|
| Grafo | explícito em Python | gravado por tracing ou eager |
| Tipos | escalar `float` | tensores N-D em GPU |
| Autograd | manual por operação | regras registradas + fusion |
| Otimizador | SGD manual | Adam, LAMB, schedulers |

O princípio é o mesmo: forward grava dependências; backward aplica regras locais na ordem reversa.

## 9. Passo a passo guiado

1. Calcule o exemplo numérico em papel.
2. Complete `starter/python/linear_train.py` (`AI-PY-GRAD-01`, `AI-PY-SGD-01`).
3. Repita em `starter/src/linear_train.c`.
4. Corrija `debug_bug.py` observando onde `x` deve aparecer.
5. Implemente `autograd_scalar.py` e valide com gradient check.
6. Compare com `solutions/python/reference_pytorch.py` se disponível.

## 10. Como saber se está correto

Após 1000 épocas na referência C:

```text
w ≈ 2.004861  b ≈ 0.985708  mse ≈ 0.000034
```

Testes: `python starter/tests/test_autograd.py`.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
