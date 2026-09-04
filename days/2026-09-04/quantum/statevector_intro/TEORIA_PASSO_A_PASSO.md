# Teoria passo a passo — State-vector simulator

## 1. Estado
Um qubit puro é `alpha|0> + beta|1>`, com `|alpha|²+|beta|²=1`. Dois qubits precisam de 4 amplitudes; n qubits, 2^n.

## 2. Representação
Usamos `std::vector<std::complex<double>>`. Estado inicial |00...0> significa `state_[0]=1` e o restante zero.

## 3. Gate como matriz 2x2
Para um par de amplitudes `(a0,a1)` do qubit alvo:

```text
new0 = m00*a0 + m01*a1
new1 = m10*a0 + m11*a1
```

## 4. Pareamento de índices
`bit = 1<<qubit`. Percorremos blocos de `step=2*bit`; dentro de cada bloco pareamos índice com bit 0 e o parceiro com bit 1.

## 5. Gates
X = [[0,1],[1,0]]; Z = [[1,0],[0,-1]]; H = 1/sqrt(2)*[[1,1],[1,-1]].

## 6. CNOT
Só troca amplitudes quando control=1 e target=0, evitando fazer o swap duas vezes.

## 7. Limite de memória
Cada `complex<double>` geralmente ocupa 16 bytes. 24 qubits => 16,777,216 amplitudes, cerca de 256 MiB apenas para o vetor. O limite do exercício evita explosão acidental.
