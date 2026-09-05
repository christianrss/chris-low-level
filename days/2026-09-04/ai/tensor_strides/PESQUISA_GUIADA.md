# Pesquisa guiada — Tensor, shape e strides

## Referência principal
NumPy documenta `ndarray.strides` como a quantidade de bytes necessária para avançar em cada dimensão:
https://numpy.org/devdocs/reference/generated/numpy.ndarray.strides.html

Depois da sua implementação, compare conceitualmente com `Tensor.stride()` do PyTorch, sem usá-lo como solução.

## Pesquise
- `numpy ndarray strides contiguous memory`
- `row major matrix offset formula`
- `transpose view zero copy`
- `matrix multiplication loop order cache locality`

## Perguntas antes do código
1. Para matriz 2x3 row-major, quais são os strides em **elementos**? E em bytes para `float` de 4 bytes?
2. Por que trocar apenas `shape` e `strides` pode representar uma transposição sem copiar dados?
3. Por que uma view transposta pode ser correta e ainda assim mais lenta?
4. Qual condição de shapes precisa ser verdadeira para `A(MxK) * B(KxN)`?

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
