# Testes guiados — typescript_stream_backpressure

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
node --experimental-strip-types --test starter/tests/*.test.ts
```

**Antes de implementar:** starter falha no framing porque mantém todos os bytes em `#pending`.

## Mapa TODO → teste

### `D2-NODE-FRAME-LINES`
- Arquivo: `starter/src/line-framer.ts`
- Validação: extrai linhas completas por `0x0A`, preserva remainder e mantém bytes UTF-8 intactos entre chunks.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-NODE-FRAME-LINES`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- 4 testes passam: chunks arbitrários, limite, linha vazia e UTF-8 multibyte dividido.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
