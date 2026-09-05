# Exercícios — State-vector simulator

## Fácil

- **D2-QSIM-SINGLE:** implemente `apply_single` percorrendo pares `(zero, one)` com `bit` e `step`.
- Calcule manualmente H(|0>) e verifique norma 1.

## Médio

- **D2-QSIM-X:** implemente Pauli-X via `apply_single`.
- **D2-QSIM-H:** implemente Hadamard com fator `1/sqrt(2)`.
- **D2-QSIM-Z:** implemente Pauli-Z.

## Difícil

- **D2-QSIM-CNOT:** troque amplitudes somente quando control=1 e target=0 no índice representante.
- Desenhe tabela de índices 0..3 e execute H(0)+CNOT(0,1) no papel.

## Desafio

- Rode benchmark com diferentes contagens de qubits e registre bytes do state vector vs gates/s.
- Pesquise limite de qubits em simuladores comerciais e relacione com 2^n.
