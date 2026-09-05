# Testes guiados — graphics_reference

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; `Surface::index`/compositor incompletos fazem o teste falhar.

## Mapa TODO → teste

### `D2-GFX-INDEX`
- Arquivo: `starter/src/graphics.cpp`
- Validação: pixel `(x,y)` deve mapear corretamente e rejeitar fora da surface.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-GFX-INDEX`

### `D2-GFX-FILL-RECT`
- Arquivo: `starter/src/graphics.cpp`
- Validação: `fill_rect(-1,-1,3,3)` altera apenas a área visível.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-GFX-FILL-RECT`

### `D2-GFX-ALPHA-OVER`
- Arquivo: `starter/src/graphics.cpp`
- Validação: azul 50% sobre vermelho produz aproximadamente `(127,0,128)`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-GFX-ALPHA-OVER`

### `D2-GFX-COMPOSE`
- Arquivo: `starter/src/graphics.cpp`
- Validação: layers são aplicadas em ordem, com offsets e clipping.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-GFX-COMPOSE`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-os graphics reference tests passed`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
