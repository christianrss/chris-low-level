# Testes guiados

O teste envia `a`, linha vazia, `b€` com o euro dividido entre chunks e `c` sem newline final. Esperado: `['a','','b€','c']`. O teste também cria Writable com `highWaterMark=8` e confirma `falseWrites > 0` e `drains == falseWrites`. A solution imprime `OK node streams`.