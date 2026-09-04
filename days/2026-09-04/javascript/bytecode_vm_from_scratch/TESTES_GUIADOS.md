# Testes guiados
O teste principal executa:
```js
let x = 10;
let y = 20;
print(x + y * 2);
print((y - x) * 3);
```
Saídas esperadas: `50` e `30`.

Também há um teste negativo: `let = 1;` deve gerar erro de sintaxe.

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```
Depois crie seus casos: precedência, parênteses aninhados, variável desconhecida (decida a semântica antes de implementar) e integer overflow como tema de design futuro.
