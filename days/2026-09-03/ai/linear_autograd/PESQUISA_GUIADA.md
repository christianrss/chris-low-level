# Pesquisa guiada — gradientes, autograd e SGD

## Objetivo
Entender a matemática e o mecanismo de autodiferenciação antes de comparar a implementação com frameworks.

## Fontes de referência
1. Documentação do PyTorch: `torch.autograd` e notas sobre automatic differentiation.
2. Cálculo diferencial: regra da cadeia e derivada de função quadrática.
3. Código educacional de autograd escalar (apenas como referência arquitetural, depois da tentativa).

## Termos de busca
- `reverse mode automatic differentiation computational graph`
- `chain rule scalar autograd`
- `mean squared error gradient linear regression`

## Perguntas antes de implementar
1. Por que `dL/dw` contém `x` em `prediction = w*x+b`?
2. Por que gradientes devem usar `+=` quando um nó participa de mais de um caminho?
3. Por que a ordem topológica é necessária no backward?
4. O que muda na escala do gradiente quando usamos soma em vez de média do batch?

## Regra de uso
Não copie uma implementação de framework. Use as fontes para validar derivadas, invariantes e vocabulário; implemente o exercício a partir do starter e da resolução guiada.
