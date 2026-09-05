# Resolução guiada passo a passo — Tensor, strides e matmul

## Mapa exato starter → resolução

- `D2-TENSOR-VIEW-AT` → `starter/src/tensor.cpp`
- `D2-TENSOR-VIEW` → `starter/src/tensor.cpp`
- `D2-TENSOR-TRANSPOSE` → `starter/src/tensor.cpp`
- `D2-TENSOR-MATMUL` → `starter/src/tensor.cpp`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

## 0. Baseline

```bash
cmake -S days/2026-09-04/ai/tensor_strides/starter -B days/2026-09-04/ai/tensor_strides/starter/build
cmake --build days/2026-09-04/ai/tensor_strides/starter/build
ctest --test-dir days/2026-09-04/ai/tensor_strides/starter/build --output-on-failure
```

Build passa; testes falham enquanto os TODOs existirem.

## Fácil — `TensorView2D::at`
Abra `starter/src/tensor.cpp`. Localize `TensorView2D::at`.

Primeiro valide:

```cpp
if (row >= rows || col >= cols || data == nullptr) {
    throw std::out_of_range("tensor view index outside range");
}
```

Depois calcule o elemento:

```cpp
return data[row * row_stride + col * col_stride];
```

Trace: na transposta da matriz 2x3, `row_stride=1`, `col_stride=3`. Para `(2,1)`: `2*1 + 1*3 = 5`, que aponta para o sexto valor, `6`.

## Médio A — view contígua
Localize `Tensor2D::view()` e retorne:

```cpp
return {data_.data(), rows_, cols_, cols_, 1};
```

A ordem do aggregate é exatamente a ordem dos campos em `TensorView2D` no header.

## Médio B — transpose view
Localize `Tensor2D::transpose_view()` e escreva:

```cpp
return {data_.data(), cols_, rows_, 1, cols_};
```

Não há `std::vector` novo: isso é zero-copy.

## Difícil — matmul
Localize `matmul`.

### Passo 1: validar shapes

```cpp
if (left.cols != right.rows) {
    throw std::invalid_argument("matmul inner dimensions do not match");
}
```

### Passo 2: criar saída

```cpp
Tensor2D out(left.rows, right.cols);
```

### Passo 3: loops i-k-j

```cpp
for (std::size_t i = 0; i < left.rows; ++i) {
    for (std::size_t k = 0; k < left.cols; ++k) {
        const float a = left.at(i, k);
        for (std::size_t j = 0; j < right.cols; ++j) {
            out.at(i, j) += a * right.at(k, j);
        }
    }
}
```

### Passo 4: retornar

```cpp
return out;
```

## Faça uma multiplicação manual antes do teste
Para:

```text
A = [1 2 3]    B = [7  8]
    [4 5 6]        [9 10]
                     [11 12]
```

`C[0,0] = 1*7 + 2*9 + 3*11 = 58`.

## Testes

```bash
cmake --build days/2026-09-04/ai/tensor_strides/starter/build
ctest --test-dir days/2026-09-04/ai/tensor_strides/starter/build --output-on-failure
```

Esperado:

```text
chris-tensor tests passed
100% tests passed
```

## Debugging
Se `transposed.at(2,1)` não for 6, inspecione `rows`, `cols`, `row_stride`, `col_stride` e o offset calculado. Se matmul der 64 onde deveria 58, escreva em papel os valores de `i`, `k`, `j`, `a` e `right.at(k,j)`.

Breakpoint sugerido: linha `out.at(i, j) += ...` e condição `i==0 && j==0`.

## Benchmark e investigação
Compile com benchmarks:

```bash
cmake -S days/2026-09-04/ai/tensor_strides/starter -B days/2026-09-04/ai/tensor_strides/starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build days/2026-09-04/ai/tensor_strides/starter/build-bench
./days/2026-09-04/ai/tensor_strides/starter/build-bench/chris_tensor_benchmark
```

Depois, como extensão, implemente versões `ijk` e `ikj`, use a mesma matriz/seed/repetições e compare. Explique cache locality antes de concluir que uma ordem é “sempre melhor”.


## Solução final comentada
Depois de deixar o starter verde, compare somente os blocos `PEDAGOGY-SOLUTION` em `solutions/` correspondentes aos IDs do mapa. Se houver uma linha necessária no gabarito que não foi ensinada acima, trate como defeito do material e não como algo que você deveria adivinhar.
