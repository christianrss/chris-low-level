# Teoria passo a passo — State-vector simulator

## 1. O problema de produção

Simuladores quânticos clássicos representam o estado como vetor de amplitudes complexas. Para n qubits há 2ⁿ amplitudes — exato e didático até ~20–24 qubits; depois a RAM explode. Este lab implementa o kernel CPU de gates 1-qubit e CNOT.

### O quê

`StateVector` com `apply_single` (matriz 2×2), wrappers `X`/`H`/`Z`, e `apply_cnot` por bitmask — estado inicial `|00…0⟩`.

### Como

Parear índices que diferem só no bit do qubit alvo (`bit=1<<q`, `step=2*bit`); aplicar `new = M · (a0,a1)` com cópias. CNOT: swap quando control=1 e target=0 no índice.

### Por quê

Sem cópias `a0/a1`, overwrite corrompe o par. Sem `target_off`, swap duplo cancela CNOT. Sem `1/√2` em H, norma deixa de ser 1 — Bell e medições mentem.

## 2. Estado e crescimento

| qubits | amplitudes | bytes (~16 B/amp) |
|-------:|-----------:|------------------:|
| 2 | 4 | 64 |
| 8 | 256 | 4 KiB |
| 16 | 65536 | 1 MiB |
| 20 | ~1M | 16 MiB |
| 24 | ~16M | 256 MiB |

## 3. Gate 2×2

```text
new0 = m00*a0 + m01*a1
new1 = m10*a0 + m11*a1
```

| Gate | Matriz | \|0⟩ → | \|1⟩ → |
|------|--------|--------|--------|
| X | [[0,1],[1,0]] | \|1⟩ | \|0⟩ |
| Z | [[1,0],[0,-1]] | \|0⟩ | −\|1⟩ |
| H | (1/√2)[[1,1],[1,-1]] | superposição | superposição |

## 4. Pareamento

```text
2 qubits, alvo=1 (bit=2, step=4)
índices 00 01 10 11 → pares (0,2) e (1,3)
```

H no qubit 0 de `|00⟩=[1,0,0,0]`:

```text
par (0,2): → [1/√2, 0, 1/√2, 0]
```

## 5. CNOT e Bell

```text
H(0); CNOT(0,1) → (|00⟩+|11⟩)/√2
P(00)=P(11)=0.5, norma=1
```

## 6. Invariantes

| Invariante | Checagem |
|------------|----------|
| Σ\|amp\|² = 1 | após gates unitários |
| `size == 2^n` | construtor |
| qubit ∈ `[0,n)` | `check_qubit` |
| control ≠ target | CNOT |

## 7. Bugs clássicos

1. Sobrescrever `a0` antes de calcular `a1`.
2. Swap CNOT duas vezes no mesmo par.
3. H sem `1/√2`.
4. Confundir endianness de bits no índice.
5. Tratar CNOT como dois gates 1-qubit.

## 8. Comparação

| Aspecto | Lab | Qiskit | Hardware |
|---------|-----|--------|----------|
| Rep | state vector | vários | físico |
| Limite | ~20–24 | +opts | ruído |
| Gates | X,H,Z,CNOT | ampla | nativos |

## 9. Probabilidade

`P(i) = |state_[i]|²`. Medição real colapsa; o lab pode só reportar probs. Bell exige P(00)=P(11)=0.5.

## 10. Complexidade

Gate 1-qubit / CNOT ingênuo: O(2ⁿ). Circuito com g gates: O(g·2ⁿ). Por isso simulação clássica explode.

## 11. Circuito Bell

```text
q0: --H--*--
         |
q1: -----X--
```

## 12. Perguntas

1. Bytes para 10 qubits?
2. Por que copiar `a0`/`a1`?
3. Qual índice é `|11⟩`?

## Fundamentos adicionais (reforço Dia 01)

### O quê

Um statevector representa amplitudes complexas; portas são matrizes unitárias aplicadas ao vetor.

### Como

Trabalhe com um exemplo numérico no papel antes de editar o starter: anote entradas, estado intermediário e saída esperada.

### Por quê

Sem o modelo mental no papel, o código vira tentativa-e-erro e os testes não ensinam o invariante.

### Por quê comparar com produção

Implementações reais (libc, kernels, VMs, GPUs) usam as mesmas ideias com mais camadas; este lab isola o núcleo.

### Por quê falhar de propósito no starter

O starter compila e o teste falha até o TODO existir — isso prova que o harness mede o comportamento certo.

### Trace manual

`	ext
entrada -> transformação -> invariante -> saída
` 

### Bugs comuns (módulo)

| Sintoma | Causa | Depuração |
|---------|-------|-----------|
| Teste falha após 'implementar' | Off-by-one / endian | Trace byte a byte |
| PASS sem entender | Copiou gabarito | Refaça o paper-trace |

