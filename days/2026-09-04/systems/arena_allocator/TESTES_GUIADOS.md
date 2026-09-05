# Testes guiados — arena_allocator

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; `allocate`/alinhamento incompletos fazem o teste falhar.

## Mapa TODO → teste

### `D2-ARENA-POWER2`
- Arquivo: `starter/src/arena.cpp`
- Validação: alignment 3 deve ser rejeitado; 8/32 devem funcionar.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-ARENA-POWER2`

### `D2-ARENA-ALIGN-UP`
- Arquivo: `starter/src/arena.cpp`
- Validação: ponteiros retornados precisam respeitar 8 e 32 bytes.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-ARENA-ALIGN-UP`

### `D2-ARENA-ALLOCATE`
- Arquivo: `starter/src/arena.cpp`
- Validação: used avança e exaustão gera `std::bad_alloc`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-ARENA-ALLOCATE`

### `D2-ARENA-RESET`
- Arquivo: `starter/src/arena.cpp`
- Validação: `reset()` volta `used()` a zero.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-ARENA-RESET`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-arena tests passed`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
