# Testes guiados
Rode:
```bash
node --experimental-strip-types --test starter/tests/*.test.ts
```
Casos:
1. `['a\\nb','eta\\nlast']` deve resultar em `['a','beta','last']`.
2. Linha sem terminador maior que limite deve rejeitar com `RangeError`.
3. Como extensão, acrescente linha vazia (`\\n`) e UTF-8 multibyte dividido entre chunks; explique o comportamento antes de alterar o código.
