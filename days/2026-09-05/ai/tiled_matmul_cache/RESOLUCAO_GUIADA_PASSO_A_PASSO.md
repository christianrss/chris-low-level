# Resolução guiada passo a passo — AI — Matmul Tiled

## Mapa exato starter → resolução

- `AI-MM-NAIVE-01` → `starter/matmul.cpp` (`matmul_naive`)
- `AI-MM-TILED-02` → `starter/matmul.cpp` (`trace_tile_4x4` e `matmul_tiled`)

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/ai/tiled_matmul_cache/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

No terminal, entre na raiz do repositório e execute:

```bash
cmake -S days/2026-09-05/ai/tiled_matmul_cache/starter -B days/2026-09-05/ai/tiled_matmul_cache/starter/build
cmake --build days/2026-09-05/ai/tiled_matmul_cache/starter/build
ctest --test-dir days/2026-09-05/ai/tiled_matmul_cache/starter/build --output-on-failure
```

O build deve funcionar. Os testes **devem falhar**: `matmul_naive` retorna zeros e `trace_tile_4x4` devolve `(0,0)` em vez de `(1,1)`. Esse é o baseline.

## `AI-MM-NAIVE-01` — multiplicação ingênua

### Arquivo

Abra:

```text
starter/matmul.cpp
```

Localize:

```cpp
std::vector<float> matmul_naive(
```

Substitua o corpo inteiro (remova os `(void)` e o `return` stub) por:

```cpp
if (a.size() != m * k || b.size() != k * n) {
    throw std::invalid_argument("shape mismatch");
}
std::vector<float> c(m * n, 0.0f);
for (std::size_t i = 0; i < m; ++i) {
    for (std::size_t j = 0; j < n; ++j) {
        float sum = 0.0f;
        for (std::size_t t = 0; t < k; ++t) {
            sum += a[i * k + t] * b[t * n + j];
        }
        c[i * n + j] = sum;
    }
}
return c;
```

Adicione no topo do arquivo, se necessário:

```cpp
#include <stdexcept>
```

### Por que funciona?

O triplo loop implementa a definição de `C[i][j] = Σ A[i][t]·B[t][j]`. Row-major garante que `A[i][t]` é `a[i*k+t]` e `B[t][j]` é `b[t*n+j]`.

### Verificação manual

Com `A = {1,2,3,4,5,6}` (2×3) e `B = {7,8,9,10,11,12}` (3×2):

```text
c[0] = 1*7 + 2*9 + 3*11 = 58
c[3] = 4*8 + 5*10 + 6*12 = 154
```

### Checkpoint

Recompile e rode `ctest`. A primeira parte do teste (trace) ainda falha, mas os asserts de `c[0]` e `c[3]` passam se você comentar temporariamente o bloco do trace — ou siga para o próximo TODO e rode tudo junto.

---

## `AI-MM-TILED-02` — `trace_tile_4x4`

### Arquivo

No mesmo `starter/matmul.cpp`, localize:

```cpp
TileTrace trace_tile_4x4(std::size_t row, std::size_t col, std::size_t tile) {
```

Substitua o `return` por:

```cpp
return {row / tile, col / tile, row, col};
```

### Por que funciona?

Divisão inteira mapeia coordenadas globais para o índice do bloco: linhas `0..tile-1` → tile 0, `tile..2*tile-1` → tile 1, etc.

### Verificação manual

```text
trace_tile_4x4(5, 7, 4) → tile_row=1, tile_col=1, global_row=5, global_col=7
```

### Checkpoint

O assert inicial de `test_matmul.cpp` (`tile_row == 1`) deve passar após recompilar.

---

## `AI-MM-TILED-02` — `matmul_tiled`

### Arquivo

Localize:

```cpp
std::vector<float> matmul_tiled(
```

Substitua o corpo por:

```cpp
if (a.size() != m * k || b.size() != k * n) {
    throw std::invalid_argument("shape mismatch");
}
if (tile == 0) {
    throw std::invalid_argument("tile must be > 0");
}

std::vector<float> c(m * n, 0.0f);
for (std::size_t ii = 0; ii < m; ii += tile) {
    for (std::size_t kk = 0; kk < k; kk += tile) {
        for (std::size_t jj = 0; jj < n; jj += tile) {
            for (std::size_t i = ii; i < std::min(ii + tile, m); ++i) {
                for (std::size_t t = kk; t < std::min(kk + tile, k); ++t) {
                    const float a_val = a[i * k + t];
                    for (std::size_t j = jj; j < std::min(jj + tile, n); ++j) {
                        c[i * n + j] += a_val * b[t * n + j];
                    }
                }
            }
        }
    }
}
return c;
```

Adicione, se necessário:

```cpp
#include <algorithm>
```

### Por que funciona?

Cada bloco `(ii,kk,jj)` acumula a mesma contribuição que o naive somaria, só que reordenada. `a_val` fica em registrador enquanto `j` varre o tile de colunas; `+=` preserva somas parciais de tiles anteriores.

### Verificação manual

Para matriz 3×5 · 5×4 com `tile=2`, confira que `|naive[i] - tiled[i]| < 1e-5` para todo `i` (o teste faz isso automaticamente).

### Checkpoint

Todos os asserts de equivalência e o teste 64×64 devem passar.

---

## Rode os testes novamente

```bash
cmake --build days/2026-09-05/ai/tiled_matmul_cache/starter/build
ctest --test-dir days/2026-09-05/ai/tiled_matmul_cache/starter/build --output-on-failure
```

Saída esperada contém:

```text
OK matmul
100% tests passed
```

## Como depurar se falhar

- `c[0]` ou `c[3]` errados: breakpoint no loop interno; confira `i*k+t` e `t*n+j`.
- `trace.tile_row != 1`: você usou `%` em vez de `/`, ou esqueceu de propagar `row`/`col` globais.
- Tiled diverge do naive: procure `=` onde deveria ser `+=`, ou `min` faltando nas bordas.
- 64×64 falha com diff grande: quase sempre índice trocado (`k` vs `n`).

## Benchmark (opcional)

Depois dos testes verdes, compare tempos em `solutions/bench_matmul.cpp`. Hipótese antes de rodar: *para 64×64 ou maior, tiled com tile=8 deve reduzir tempo vs naive em CPU com cache pequena*.

## Solução final comentada

Compare `starter/matmul.cpp` com `solutions/matmul.cpp`. Você deve justificar: validação de shape, ordem dos seis loops, uso de `+=`, e divisão inteira no trace.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| AI-MM-NAIVE-01 | `matmul.cpp` | `c[0]=58`, `c[3]=154` no caso 2×3·3×2 |
| AI-MM-TILED-02 | `matmul.cpp` | `trace(5,7,4)` → tile (1,1); tiled ≡ naive em 3×5 e 64×64 |

Critério de aceite: `ctest` reporta `OK matmul` e 100% dos testes.

### Template do relatório

```
Aluno:
Módulo: AI — Matmul Tiled
Data:

1. TODOs: AI-MM-NAIVE-01, AI-MM-TILED-02
2. Primeira falha: [ex.: assert c[0]==58 com vetor de zeros]
3. Correção aplicada: [ex.: triplo loop row-major + tiling com +=]
4. Evidência: [colar saída OK matmul / 100% tests passed]
```
