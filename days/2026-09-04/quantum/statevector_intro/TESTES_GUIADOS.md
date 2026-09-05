# Testes guiados — statevector_intro

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; gates incompletos fazem probabilidades falharem.

## Mapa TODO → teste

### `D2-QSIM-SINGLE`
- Arquivo: `starter/src/qsim.cpp`
- Validação: kernel 2x2 preserva norma para X/H/Z.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-QSIM-SINGLE`

### `D2-QSIM-X`
- Arquivo: `starter/src/qsim.cpp`
- Validação: X transforma `|0>` em `|1>`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-QSIM-X`

### `D2-QSIM-H`
- Arquivo: `starter/src/qsim.cpp`
- Validação: H gera probabilidades `0.5/0.5`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-QSIM-H`

### `D2-QSIM-Z`
- Arquivo: `starter/src/qsim.cpp`
- Validação: Z preserva probabilidades/norma após X.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-QSIM-Z`

### `D2-QSIM-CNOT`
- Arquivo: `starter/src/qsim.cpp`
- Validação: H(0)+CNOT(0,1) gera Bell em índices 0 e 3.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-QSIM-CNOT`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-qsim tests passed`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
