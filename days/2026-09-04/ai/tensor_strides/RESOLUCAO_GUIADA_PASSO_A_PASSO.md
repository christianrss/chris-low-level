# RESOLUÇÃO GUIADA — AI / Tensor, strides e matmul

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `D2-TENSOR-VIEW-AT` | `starter/src/tensor.cpp` | `TensorView2D::at` |
| `D2-TENSOR-VIEW` | `starter/src/tensor.cpp` | `Tensor2D::view` |
| `D2-TENSOR-TRANSPOSE` | `starter/src/tensor.cpp` | `Tensor2D::transpose_view` |
| `D2-TENSOR-MATMUL` | `starter/src/tensor.cpp` | `matmul` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-04/ai/tensor_strides/starter/`. `solutions/` é gabarito.

Campos de `TensorView2D` (ordem do aggregate no header):

```text
data, rows, cols, row_stride, col_stride
```

Strides são em **elementos**, não bytes.

---

## Baseline

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Build passa; testes falham enquanto os TODOs existirem.

---

## Exercício Fácil — `D2-TENSOR-VIEW-AT`

### 1. O problema

`TensorView2D::at` no starter lança `logic_error("TODO...")`. Sem índice por stride, views e transpose não têm como ler o storage.

### 2. O algoritmo

```text
se row >= rows ou col >= cols ou data == nullptr:
  throw out_of_range
return data[row * row_stride + col * col_stride]
```

### 3. Escreva o código

```cpp
if (row >= rows || col >= cols || data == nullptr) {
    throw std::out_of_range("tensor view index outside range");
}
return data[row * row_stride + col * col_stride];
```

### 4. Por que funciona

Uma fórmula serve para qualquer layout 2D sobre o mesmo buffer:

| Layout | row_stride | col_stride |
|--------|----------:|-----------:|
| Contígua 2×3 | 3 | 1 |
| Transposta 3×2 | 1 | 3 |

Trace — dados `[1,2,3,4,5,6]`, view transposta `(rows=3,cols=2,rs=1,cs=3)`:

```text
at(2,1) = 2*1 + 1*3 = 5 → valor 6
```

### 5. Verifique

Ainda dependerá de `view`/`transpose_view` para o teste de integração; compile após cada função.

---

## Exercício Médio A — `D2-TENSOR-VIEW`

### 1. O problema

`view()` deve expor a matriz dona como view contígua row-major **sem copiar** `data_`.

### 2. O algoritmo

Para shape `rows_ × cols_` armazenado row-major:

```text
row_stride = cols_   # pular uma linha
col_stride = 1       # elemento seguinte na linha
```

### 3. Escreva o código

```cpp
return {data_.data(), rows_, cols_, cols_, 1};
```

### 4. Por que funciona

`data_.data()` aponta ao início do `vector`. Metadados só reinterpretam geometria. Teste espera `plain.row_stride == 3 && plain.col_stride == 1` na matriz 2×3.

### 5. Verifique

Após implementar `at` + `view`, acessos contíguos devem bater com `Tensor2D::at`.

---

## Exercício Médio B — `D2-TENSOR-TRANSPOSE`

### 1. O problema

`transpose_view()` não deve alocar `std::vector` novo. Troca shape e strides.

### 2. O algoritmo

```text
original:  rows=R cols=C  strides=(C, 1)
transpose: rows=C cols=R  strides=(1, C)
mesmo ponteiro data_
```

### 3. Escreva o código

```cpp
return {data_.data(), cols_, rows_, 1, cols_};
```

### 4. Por que funciona

`at(i,j)` na transposta lê `data[i*1 + j*cols_]` ≡ elemento original `(j,i)`. Zero-copy: só metadados mudam.

```text
original 2×3:        transpose view 3×2:
1 2 3                1 4
4 5 6                2 5
                     3 6
```

### 5. Verifique

`transposed.at(2,1) == 6` no teste.

---

## Exercício Difícil — `D2-TENSOR-MATMUL`

### 1. O problema

`matmul` deve computar `C = A × B` sobre **views** (podem ser transpostas), validar dimensão interna e usar ordem de loop `i-k-j`.

### 2. O algoritmo

```text
se left.cols != right.rows: invalid_argument
out = Tensor2D(left.rows, right.cols)   # zeros
para i em [0, left.rows):
  para k em [0, left.cols):
    a = left.at(i, k)
    para j em [0, right.cols):
      out.at(i, j) += a * right.at(k, j)
return out
```

### 3. Escreva o código

```cpp
if (left.cols != right.rows) {
    throw std::invalid_argument("matmul inner dimensions do not match");
}

Tensor2D out(left.rows, right.cols);
for (std::size_t i = 0; i < left.rows; ++i) {
    for (std::size_t k = 0; k < left.cols; ++k) {
        const float a = left.at(i, k);
        for (std::size_t j = 0; j < right.cols; ++j) {
            out.at(i, j) += a * right.at(k, j);
        }
    }
}
return out;
```

### 4. Por que funciona

Matemática: `C[i,j] = Σ_k A[i,k] * B[k,j]`. Loop `i-k-j` fixa `a = A[i,k]` e reutiliza no inner `j` — menos releituras de `left` que `i-j-k`. `out` nasce zerado pelo construtor `Tensor2D(rows, cols)`.

#### Multiplicação manual (faça antes do teste)

```text
A = [1 2 3]    B = [7  8]
    [4 5 6]        [9 10]
                     [11 12]

C[0,0] = 1*7 + 2*9 + 3*11 = 58
C[0,1] = 1*8 + 2*10 + 3*12 = 64
C[1,0] = 4*7 + 5*9 + 6*11 = 139
C[1,1] = 4*8 + 5*10 + 6*12 = 154
```

O teste espera exatamente esses quatro valores e rejeita shapes incompatíveis.

### 5. Verifique

```bash
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Esperado:

```text
chris-tensor tests passed
100% tests passed
```

---

## Debugging

| Sintoma | Causa |
|---------|-------|
| `transposed.at(2,1) ≠ 6` | strides invertidos ou shape não trocado |
| matmul dá 64 onde queria 58 | índices `k`/`j` trocados; faça o papel |
| segfault / lixo | `at` sem bounds; `data == nullptr` |
| shapes incompatíveis aceitos | faltou `left.cols != right.rows` |

Breakpoint sugerido: `out.at(i, j) += ...` com condição `i==0 && j==0`.

---

## Benchmark (extensão)

```bash
cmake -S starter -B starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build starter/build-bench
./starter/build-bench/chris_tensor_benchmark
```

Compare ordens `ijk` vs `ikj` **uma variável por vez** (mesma seed, mesmas repetições). Explique locality antes de declarar um vencedor absoluto.

---

## Mapa de consistência auditada

- `D2-TENSOR-VIEW-AT` — `starter/src/tensor.cpp` → `solutions/src/tensor.cpp`
- `D2-TENSOR-VIEW` — `starter/src/tensor.cpp` → `solutions/src/tensor.cpp`
- `D2-TENSOR-TRANSPOSE` — `starter/src/tensor.cpp` → `solutions/src/tensor.cpp`
- `D2-TENSOR-MATMUL` — `starter/src/tensor.cpp` → `solutions/src/tensor.cpp`

Compare somente blocos `PEDAGOGY-SOLUTION`.

---

## Relatório de resolução

### O que foi validado

- Offset por strides com bounds check.
- View contígua `(cols, 1)` e transpose `(1, cols)` zero-copy.
- Matmul `i-k-j` com rejeição de shapes e resultado `58,64,139,154`.

### Armadilhas encontradas

- Stride em bytes vs elementos (`sizeof(float)` indevido).
- Transpor copiando dados — perde o ponto do exercício.
- Assumir contigüidade após transpose view em kernels ingênuos.

### Depuração e saída esperada

- **Depuração:** imprima `rows,cols,row_stride,col_stride` e o offset; papel para `C[0,0]`.
- **Saída esperada:** `chris-tensor tests passed`.

### Próximo passo sugerido

Registre no benchmark o efeito da ordem de loop em 256×256; depois leia como PyTorch representa tensors não-contíguos — a equivalência é exatamente `TensorView2D`.
