# Exercícios — Tensor, strides e matmul

## Fácil

- **D2-TENSOR-VIEW-AT:** implemente validação de limites e cálculo `row*row_stride + col*col_stride` em `TensorView2D::at`.
- Calcule manualmente offsets para matriz 2x3 e sua transposta 3x2 nos índices `(0,2)`, `(1,1)` e `(2,1)`.

## Médio

- **D2-TENSOR-VIEW:** retorne view contígua com strides `(cols, 1)` em `Tensor2D::view`.
- **D2-TENSOR-TRANSPOSE:** implemente transpose zero-copy trocando shape e strides sem alocar novo buffer.

## Difícil

- **D2-TENSOR-MATMUL:** valide dimensões internas e implemente matmul com ordem `i-k-j`.
- Faça multiplicação manual de A(2x3) por B(3x2) e compare com o teste automatizado.

## Desafio

- Implemente versões `i-j-k` e `i-k-j`, rode o benchmark e registre mediana. Explique diferença de locality.
- Pesquise como PyTorch representa tensor não-contíguo e descreva equivalência com `TensorView2D`.
