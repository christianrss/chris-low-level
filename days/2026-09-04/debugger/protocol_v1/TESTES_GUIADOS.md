# Testes guiados — protocol_v1

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; decode/encode incompletos fazem o teste falhar.

## Mapa TODO → teste

### `D2-DBG-APPEND-U16`
- Arquivo: `starter/src/protocol.cpp`
- Validação: round-trip preserva version/command de 16 bits.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-DBG-APPEND-U16`

### `D2-DBG-APPEND-U32`
- Arquivo: `starter/src/protocol.cpp`
- Validação: round-trip preserva request id, size e hash de 32 bits.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-DBG-APPEND-U32`

### `D2-DBG-READ-U16`
- Arquivo: `starter/src/protocol.cpp`
- Validação: decoder reconstrói campos de 16 bits little-endian.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-DBG-READ-U16`

### `D2-DBG-READ-U32`
- Arquivo: `starter/src/protocol.cpp`
- Validação: decoder reconstrói campos de 32 bits little-endian.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-DBG-READ-U32`

### `D2-DBG-FNV1A`
- Arquivo: `starter/src/protocol.cpp`
- Validação: payload corrompido deve ser rejeitado pelo hash.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-DBG-FNV1A`

### `D2-DBG-ENCODE`
- Arquivo: `starter/src/protocol.cpp`
- Validação: encode gera packet que faz round-trip completo.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-DBG-ENCODE`

### `D2-DBG-DECODE`
- Arquivo: `starter/src/protocol.cpp`
- Validação: decode aceita packet válido e rejeita header truncado/corrompido.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-DBG-DECODE`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-debugger protocol tests passed`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
