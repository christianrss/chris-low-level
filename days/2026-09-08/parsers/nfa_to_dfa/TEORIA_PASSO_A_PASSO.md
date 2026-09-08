# Teoria passo a passo — NFA to DFA

Subset construction transforma um NFA em DFA cujos estados são conjuntos de estados NFA. Antes de consumir símbolo,
cada conjunto precisa de epsilon closure. Para cada símbolo do alfabeto: move(active,symbol) coleta destinos e
closure produz o próximo conjunto DFA.

Use `frozenset` como identidade de estado. O start DFA é closure({nfa_start}). Um estado DFA é final se contém o
accept NFA.

Esse processo pode produzir até 2^N conjuntos no pior caso; por isso engines podem preferir NFA simulation ou DFA
lazy. Hoje construiremos DFA explícito e compararemos matches com o NFA do milestone anterior.
