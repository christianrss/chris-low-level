# Resolução guiada passo a passo — NFA to DFA

Edite `starter/dfa.py`.

### TODO D6-DFA-CLOSURE
DFS/BFS por edges cujo símbolo é `None`.

### TODO D6-DFA-SUBSET
Colete alfabeto excluindo epsilon. Use fila:
```python
start=frozenset(closure({nfa_start}))
queue=[start]
ids={start:0}
```
Para cada conjunto e símbolo, mova, aplique closure, intern o conjunto e crie transition.

### TODO D6-DFA-MATCH
Percorra chars usando tabela; ausência de aresta retorna False. Aceite se state id está em `accepting`.

O teste fornece NFAs pequenos, inclusive `a*` com ciclos epsilon, e compara corpus com simulador de referência.
Execute `python starter/test_dfa.py`.
