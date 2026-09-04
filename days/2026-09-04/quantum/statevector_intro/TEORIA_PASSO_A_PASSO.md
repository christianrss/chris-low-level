# Teoria passo a passo — State-vector quântico

## 1. Amplitudes complexas
Um qubit `|psi>` possui amplitudes complexas `alpha` e `beta`, com `|alpha|² + |beta|² = 1`. Essas grandezas não são probabilidades diretamente; o quadrado do módulo é a probabilidade de medição.

## 2. Crescimento exponencial
`n` qubits exigem `2^n` amplitudes. Se cada amplitude usa dois `double` (16 bytes), 30 qubits exigiriam aproximadamente 16 GiB apenas para o vetor.

## 3. Gates unitários
X troca amplitudes; Z muda a fase de `|1>`; H cria/interfere superposições. Uma operação unitária preserva a norma.

## 4. CNOT e Bell
Aplicar H no qubit 0 de `|00>` cria superposição. CNOT controlada por q0 e alvo q1 produz amplitudes apenas em `|00>` e `|11>`: um Bell state.

## 5. Exercícios
**Fácil:** calcule H|0>.  
**Médio:** implemente pares de amplitudes para gate de 1 qubit.  
**Difícil:** implemente CNOT sem duplicar swaps.  
**Desafio:** adicione medição com RNG seed e teste estatístico com tolerância justificada.
