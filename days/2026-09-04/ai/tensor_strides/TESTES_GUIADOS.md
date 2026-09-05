# Testes guiados — tensor_strides

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; teste falha enquanto os TODOs permanecem.

## Mapa TODO → teste

### `D2-TENSOR-VIEW-AT`
- Arquivo: `starter/src/tensor.cpp`
- Validação: `TensorView2D::at` resolve `(2,1)` da view transposta para `6` e valida bounds.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-TENSOR-VIEW-AT`

### `D2-TENSOR-VIEW`
- Arquivo: `starter/src/tensor.cpp`
- Validação: `view()` expõe shape `2x3`, `row_stride=3`, `col_stride=1`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-TENSOR-VIEW`

### `D2-TENSOR-TRANSPOSE`
- Arquivo: `starter/src/tensor.cpp`
- Validação: `transpose_view()` expõe `3x2` sem cópia.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-TENSOR-TRANSPOSE`

### `D2-TENSOR-MATMUL`
- Arquivo: `starter/src/tensor.cpp`
- Validação: matmul produz `58,64,139,154` e rejeita shapes incompatíveis.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-TENSOR-MATMUL`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-tensor tests passed` e `100% tests passed`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
