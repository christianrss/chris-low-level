# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/` e localize os TODOs.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Compile/teste após cada etapa.
5. Só então compare com `solutions/`.

---

# IA Low-Level - Dia 1: neurônio linear, SGD e primeiro autograd

Este módulo refaz o treino original de IA low-level em um formato mais rigoroso. O objetivo continua sendo entender o ciclo completo sem NumPy, PyTorch, TensorFlow ou autograd: `forward -> loss -> gradientes -> atualização`.

## Exercícios

### Fácil - cálculo manual
Use `x=2`, `w=3`, `b=1`, `y=10`.

1. Calcule `pred = w*x+b`.
2. Calcule `error = pred-y`.
3. Calcule `loss = error^2`.

### Médio - gradientes e SGD
Derive e calcule:

- `dL/dw = 2*(pred-y)*x`
- `dL/db = 2*(pred-y)`

Aplique um passo com `learning_rate=0.01`.

### Médio - treino sem framework
Faça o modelo aprender `y = 2x + 1` no conjunto `(1,3), (2,5), (3,7), (4,9)`.

Compare:

- Python puro em `solutions/python/linear_train.py`;
- C em `solutions/src/linear_train.c`.

### Difícil - debugging de backward
`starter/python/debug_bug.py` contém gradientes trocados. Encontre e explique os erros antes de abrir a solução.

### Desafio principal - começo do autograd
Implemente uma classe `Value` escalar que registre operações `+` e `*`, construa um DAG e propague gradientes em ordem topológica.

A solução está em `solutions/python/autograd_scalar.py`.

## Build C

Windows / Visual Studio:

```bat
cmake -S solutions -B build-solution -A x64
cmake --build build-solution --config Release
build-solution\Release\linear_train.exe
```

Linux:

```bash
cmake -S solutions -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/linear_train
```

## Testes

```bash
python solutions/tests/test_ai.py
```

Resultado de referência do treino linear: `w` próximo de `2` e `b` próximo de `1`.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-autograd` |
| O que levar | gradient ops + training loop (not lab harness) |
| Testes a replicar | gradient/regression tests in project |
| Milestone | MILESTONES.md — scalar autograd |
| Commit sugerido | `feat(autograd): port linear training from day01 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
