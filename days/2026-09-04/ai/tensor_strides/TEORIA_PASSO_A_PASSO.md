# Teoria passo a passo — Tensor, shape, strides e matmul

## 1. Dados físicos x geometria lógica
Nosso `Tensor2D` guarda floats contíguos. Uma matriz 2x3 `[1,2,3;4,5,6]` é fisicamente `[1,2,3,4,5,6]`. `rows`/`cols` descrevem forma; *strides* dizem como transformar índice lógico em offset.

## 2. Fórmula de offset
Em uma view 2D:

```text
offset = row * row_stride + col * col_stride
```

No projeto, strides são medidos em **elementos**, não bytes. Para 2x3 contígua: `(row_stride=3, col_stride=1)`.

## 3. Transpose zero-copy
A mesma memória pode ser vista como 3x2. Basta trocar dimensões e strides:

```text
original: rows=2 cols=3 row_stride=3 col_stride=1
transpose: rows=3 cols=2 row_stride=1 col_stride=3
```

## 4. Matmul
Para `C=A*B`:

```text
C[i,j] = soma_k A[i,k] * B[k,j]
```

Se A é MxK, B deve ser KxN e C será MxN.

## 5. Loop order do laboratório
Usaremos `i-k-j`. Para cada `A[i,k]`, reutilizamos o valor enquanto percorremos colunas de B/saída. É uma introdução a locality; não é um GEMM otimizado.

## 6. Invariantes
- dimensões não nulas;
- `values.size() == rows*cols`;
- índices dentro do shape;
- `left.cols == right.rows`;
- views não são donas da memória.
