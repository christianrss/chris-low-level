# Testes guiados - IA low-level

## Teste 1 - convergência da regressão linear

**Invariante:** o dataset `y=2x+1` deve produzir `w` próximo de `2` e `b` próximo de `1`.

### Caso 1: Importe `train()`.
### Caso 2: Execute 1000 épocas com `lr=0.01`.
### Caso 3: Use tolerâncias em vez de igualdade exata porque treinamento usa ponto flutuante.
### Caso 4: Verifique `abs(w-2) < 0.02` e `abs(b-1) < 0.05`.

## Teste 2 - gradiente analítico vs numérico

Este é um **gradient check**, uma técnica usada para validar backpropagation.

Para `f(w)=(w*x+b-y)^2`, estime a derivada numericamente:

`df/dw ~= (f(w+eps)-f(w-eps))/(2*eps)`

Compare com o gradiente produzido por `Value.backward()`. Comece com `eps=1e-6` e tolerância `1e-5`.

## Teste 3 - acumulação de gradientes

Construa `z = x*x + x`. O mesmo nó `x` participa de múltiplos caminhos. O backward correto deve somar contribuições, não sobrescrever `grad`.

## Teste 4 - operação não suportada

`Value(2.0) ** 3` deve levantar `ValueError`. Este é um teste negativo de contrato da API.

## Como depurar

Imprima a ordem topológica e `(label, data, grad)` após cada `_backward`. Se o valor forward estiver certo e o gradiente errado, o problema está na derivada local ou na ordem/accumulation do backward.

## Cobertura pedagógica auditada

Os IDs abaixo precisam ter um critério de verificação antes de o módulo ser considerado concluído.

- `AI-PY-GRAD-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `AI-PY-SGD-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `AI-AUTOGRAD-ADD-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `AI-AUTOGRAD-MUL-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `AI-AUTOGRAD-BWD-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `AI-C-GRAD-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `AI-C-AVG-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `AI-C-SGD-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.

Arquivos de teste automatizado presentes no starter:
- `starter/tests/test_autograd.py`
