# RESOLUÇÃO GUIADA - IA low-level / Linear + Autograd

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `AI-AUTOGRAD-ADD-01` | `starter/python/autograd_scalar.py` | `Value.__add__` |
| `AI-AUTOGRAD-MUL-01` | `starter/python/autograd_scalar.py` | `Value.__mul__` |
| `AI-AUTOGRAD-BWD-01` | `starter/python/autograd_scalar.py` | `backward()` (travessia topológica) |
| `AI-PY-GRAD-01` | `starter/python/linear_train.py` | `train()` — acumular dL/dw e dL/db |
| `AI-PY-SGD-01` | `starter/python/linear_train.py` | `train()` — média do batch + update SGD |
| `AI-C-GRAD-01` | `starter/src/linear_train.c` | `main()` — acumular gradientes no loop |
| `AI-C-AVG-01` | `starter/src/linear_train.c` | `main()` — média dos gradientes |
| `AI-C-SGD-01` | `starter/src/linear_train.c` | `main()` — passo SGD |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/ai/linear_autograd/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## Exercício Fácil - calcular forward, erro, loss e um passo de SGD

Dados:

```text
x = 2
w = 3
b = 1
y = 10
learning_rate = 0.01
```

### 1. Forward

A fórmula é:

```text
prediction = w*x + b
```

Substituindo:

```text
prediction = 3*2 + 1 = 7
```

### 2. Erro

```text
error = prediction - y = 7 - 10 = -3
```

O sinal negativo significa que a previsão ficou abaixo do alvo.

### 3. Loss

```text
loss = error^2 = (-3)^2 = 9
```

### 4. Gradiente de w

A loss é:

```text
L = (w*x + b - y)^2
```

Pela regra da cadeia:

```text
dL/dw = 2*(prediction-y)*x
       = 2*(-3)*2
       = -12
```

### 5. Gradiente de b

```text
dL/db = 2*(prediction-y)
       = 2*(-3)
       = -6
```

### 6. Atualização SGD

```text
w_new = 3 - 0.01*(-12) = 3.12
b_new = 1 - 0.01*(-6)  = 1.06
```

O gradiente era negativo, então subtrair um número negativo aumenta os parâmetros.

---

## Exercício Médio A - treinar y=2x+1 em Python

Abra:

```text
starter/python/linear_train.py
```

O dataset é:

```text
x: 1  2  3  4
y: 3  5  7  9
```

A relação real é `y = 2x + 1`.

### 1. Acumule gradientes por amostra

Dentro do loop interno, depois de `error`:

```python
d_weight += 2.0 * error * x
d_bias += 2.0 * error
```

Por que `+=`? Porque queremos a contribuição de **todas** as amostras do batch.

### 2. Faça a média

Antes de atualizar parâmetros:

```python
count = len(xs)
d_weight /= count
d_bias /= count
```

Coloque `count = len(xs)` antes do loop de épocas para não recalcular a mesma quantidade.

### 3. Atualize parâmetros

```python
weight -= learning_rate * d_weight
bias -= learning_rate * d_bias
```

### 4. Execute

```bash
python starter/python/linear_train.py
```

Depois de 1000 épocas, espere valores próximos de:

```text
w ≈ 2
b ≈ 1
```

Não precisa ser exatamente 2 e 1 por causa do número finito de épocas e learning rate.

### 5. Debug recomendado

Temporariamente imprima a cada 100 épocas:

```python
if epoch % 100 == 0:
    print(epoch, weight, bias)
```

Para isso, troque `for _ in range(epochs)` por `for epoch in range(epochs)`.

Você deve observar os parâmetros convergindo, não explodindo.

---

## Exercício Médio B - repetir em C

Abra `starter/src/linear_train.c`.

A matemática é igual. O objetivo é observar que não existe objeto Tensor escondendo memória.

### 1. Dentro do loop de amostras

```c
d_weight += 2.0 * error * x;
d_bias += 2.0 * error;
```

### 2. Média

```c
d_weight /= (double)count;
d_bias /= (double)count;
```

O cast evita depender de regras de divisão inteira caso tipos mudem.

### 3. SGD

```c
weight -= learning_rate * d_weight;
bias -= learning_rate * d_bias;
```

### 4. Build

```bash
cmake -S starter -B starter/build
cmake --build starter/build
```

No Visual Studio multi-config:

```bat
cmake -S starter -B starter\build -A x64
cmake --build starter\build --config Debug
```

---

## Exercício Difícil - corrigir o backward bugado

Abra:

```text
starter/python/debug_bug.py
```

O bug original troca as fórmulas:

```python
dw += 2 * error
db += 2 * error * x
```

### 1. Como descobrir sem decorar?

Comece pela função:

```text
prediction = w*x + b
```

A derivada da prediction em relação a `w` é `x`. Logo o gradiente de `w` precisa conter `x`.

A derivada em relação a `b` é `1`. Logo o gradiente de `b` **não** contém `x`.

### 2. Correção

```python
dw += 2.0 * error * x
db += 2.0 * error
```

### 3. Segundo problema possível

Se a loss que você diz otimizar é a **MSE média do batch**, normalize:

```python
dw /= len(xs)
db /= len(xs)
```

Sem a média, o gradiente cresce proporcionalmente ao batch size. Ainda pode treinar se o learning rate compensar, mas a escala deixa de corresponder à função definida.

---

## Desafio principal - construir autograd escalar

Abra:

```text
starter/python/autograd_scalar.py
```

### Conceito 1 - cada Value é um nó

Precisamos guardar:

- valor numérico `data`;
- gradiente `grad`;
- pais `_prev`;
- função local `_backward`.

Uma implementação conveniente usa `dataclass`:

```python
@dataclass(eq=False)
class Value:
    data: float
    label: str = ""
    grad: float = 0.0
    _prev: tuple["Value", ...] = field(default_factory=tuple, repr=False)
    _backward: Callable[[], None] = field(
        default=lambda: None,
        repr=False,
    )
```

`eq=False` permite usar identidade do objeto em um `set` durante a ordenação topológica.

### Conceito 2 - soma cria um novo nó

```python
def __add__(self, other: "Value | float") -> "Value":
    rhs = other if isinstance(other, Value) else Value(float(other))
    out = Value(self.data + rhs.data, _prev=(self, rhs))

    def backward() -> None:
        self.grad += out.grad
        rhs.grad += out.grad

    out._backward = backward
    return out
```

Por que `+=` e não `=`? Um nó pode alimentar mais de um caminho do grafo; gradientes de caminhos diferentes precisam ser somados.

### Conceito 3 - multiplicação

Para `out = a*b`:

```text
dout/da = b
dout/db = a
```

Código:

```python
def __mul__(self, other: "Value | float") -> "Value":
    rhs = other if isinstance(other, Value) else Value(float(other))
    out = Value(self.data * rhs.data, _prev=(self, rhs))

    def backward() -> None:
        self.grad += rhs.data * out.grad
        rhs.grad += self.data * out.grad

    out._backward = backward
    return out
```

### Conceito 4 - subtração reutiliza soma e multiplicação

```python
def __sub__(self, other: "Value | float") -> "Value":
    rhs = other if isinstance(other, Value) else Value(float(other))
    return self + (rhs * -1.0)
```

### Conceito 5 - quadrado

```python
def __pow__(self, power: int) -> "Value":
    if power != 2:
        raise ValueError("este exercício implementa apenas potência 2")

    out = Value(self.data * self.data, _prev=(self,))

    def backward() -> None:
        self.grad += 2.0 * self.data * out.grad

    out._backward = backward
    return out
```

### Conceito 6 - ordenação topológica

Precisamos executar o backward dos filhos antes dos pais. Construa uma lista pós-ordem:

```python
topo: list[Value] = []
visited: set[Value] = set()


def build(node: Value) -> None:
    if node in visited:
        return

    visited.add(node)
    for parent in node._prev:
        build(parent)

    topo.append(node)
```

Depois:

```python
build(self)
self.grad = 1.0

for node in reversed(topo):
    node._backward()
```

`self.grad = 1.0` porque `dL/dL = 1`.

### Teste final

```python
x = Value(2.0)
w = Value(3.0)
b = Value(1.0)
target = Value(10.0)

prediction = w * x + b
error = prediction - target
loss = error ** 2
loss.backward()
```

Resultado esperado:

```text
prediction = 7
loss = 9
dL/dw = -12
dL/db = -6
```

### Comparação opcional com PyTorch

Rode `solutions/python/reference_pytorch.py` se PyTorch já estiver instalado. O objetivo não é usar PyTorch para resolver o exercício, mas confirmar que a sua matemática manual produz os mesmos gradientes.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `AI-AUTOGRAD-ADD-01` — `starter/python/autograd_scalar.py` → `solutions/python/autograd_scalar.py`.
- `AI-AUTOGRAD-MUL-01` — `starter/python/autograd_scalar.py` → `solutions/python/autograd_scalar.py`.
- `AI-AUTOGRAD-BWD-01` — `starter/python/autograd_scalar.py` → `solutions/python/autograd_scalar.py`.
- `AI-PY-GRAD-01` — `starter/python/linear_train.py` → `solutions/python/linear_train.py`.
- `AI-PY-SGD-01` — `starter/python/linear_train.py` → `solutions/python/linear_train.py`.
- `AI-C-GRAD-01` — `starter/src/linear_train.c` → `solutions/src/linear_train.c`.
- `AI-C-AVG-01` — `starter/src/linear_train.c` → `solutions/src/linear_train.c`.
- `AI-C-SGD-01` — `starter/src/linear_train.c` → `solutions/src/linear_train.c`.

## Relatório de resolução

Checklist ao concluir:

- [ ] Python (`AI-PY-GRAD-01`, `AI-PY-SGD-01`) e C (`AI-C-GRAD-01`, `AI-C-AVG-01`, `AI-C-SGD-01`) convergem para `w≈2`, `b≈1`.
- [ ] Autograd (`AI-AUTOGRAD-*`) reproduz `dL/dw=-12`, `dL/db=-6` no exemplo fixo.
- [ ] `starter/python/debug_bug.py` corrigido sem consultar gabarito primeiro.
- [ ] `python starter/tests/test_autograd.py` passa.

**Depuração:** imprima `weight`, `bias` a cada 100 épocas; gradientes devem diminuir de magnitude, não explodir.

**Arquivos starter editados:** `starter/python/linear_train.py`, `starter/python/autograd_scalar.py`, `starter/src/linear_train.c`.
