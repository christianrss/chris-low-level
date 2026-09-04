# Teoria passo a passo — Tensor, shape e strides

## 1. Tensor não é só `vector<float>`
Uma matriz 2x3 pode ser armazenada como seis floats. `shape=(2,3)` diz a geometria lógica; `strides` dizem quantos elementos avançar na memória ao mudar um índice.

## 2. Row-major
Para uma matriz contígua row-major, `row_stride=cols` e `col_stride=1`. O elemento `(r,c)` vive em `r*row_stride + c*col_stride`.

## 3. Transpose view
Uma transposição pode trocar shape e strides sem mover bytes: `(rows, cols, cols, 1)` vira `(cols, rows, 1, cols)`. Isso é zero-copy, mas o padrão de acesso pode ficar ruim para cache.

## 4. Matmul
Para `C=A*B`, `C[i,j]=sum_k A[i,k]*B[k,j]`. O algoritmo ingênuo custa aproximadamente `2*M*N*K` operações de ponto flutuante.

## 5. Exercícios
**Fácil:** derive os offsets de uma matriz 2x3.  
**Médio:** implemente `transpose_view`.  
**Difícil:** implemente matmul aceitando views.  
**Desafio:** compare loop orders `ijk`, `ikj` e uma versão com `B` transposta, medindo cache/performance.
