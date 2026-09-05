# Exercícios — IA linear + autograd escalar

## Fácil

- **AI-MANUAL-01:** com `x=2, w=3, b=1, y=10`, calcule `prediction`, `error`, `loss`, `dL/dw` e `dL/db` em papel.
- **AI-PY-GRAD-01:** complete o acúmulo de gradientes em `starter/python/linear_train.py`.
- **AI-C-GRAD-01:** replique a mesma lógica em `starter/src/linear_train.c`.

## Médio

- **AI-PY-SGD-01:** aplique média do batch e atualização SGD em Python; espere `w≈2`, `b≈1` após 1000 épocas.
- **AI-C-AVG-01 / AI-C-SGD-01:** finalize o loop C com média e SGD; compare saída com Python.
- **AI-DEBUG-01:** encontre e corrija o bug em `starter/python/debug_bug.py` sem olhar o gabarito.

## Difícil

- **AI-AUTOGRAD-ADD-01 / AI-AUTOGRAD-MUL-01:** implemente `__add__` e `__mul__` com closures de backward corretas.
- **AI-AUTOGRAD-BWD-01:** implemente `backward()` com ordenação topológica e `grad` inicial 1.0.
- **AI-GRADCHECK-01:** valide `w.grad` contra diferença numérica finita no teste.

## Desafio

- **AI-GRAPH-01:** desenhe o grafo completo de `(w*x+b-target)²` e marque o valor de `grad` em cada nó após `backward()`.
- **AI-EXT-01:** explique como você adicionaria `ReLU` sem quebrar a API atual de `Value`.
