# Teoria passo a passo — State-vector simulator

## 1. Estado quântico

Um qubit puro é `alpha|0> + beta|1>`, com `|alpha|²+|beta|²=1`. Dois qubits precisam de 4 amplitudes; n qubits, 2^n.

Este simulador usa **state vector** clássico: representamos amplitudes complexas em `std::vector<std::complex<double>>`. É exato para poucos qubits e didático; não escala como hardware quântico real.

## 2. Representação

Usamos `std::vector<std::complex<double>>`. Estado inicial |00...0> significa `state_[0]=1` e o restante zero.

### Tabela de crescimento

| qubits | amplitudes | bytes (~16 B/amp) |
|-------:|-----------:|------------------:|
| 2      | 4          | 64                |
| 8      | 256        | 4 KiB             |
| 16     | 65536      | 1 MiB             |
| 20     | 1 048 576  | 16 MiB            |
| 24     | 16 777 216 | 256 MiB           |

O limite do exercício evita explosão acidental de memória.

## 3. Gate como matriz 2x2

Para um par de amplitudes `(a0,a1)` do qubit alvo:

```text
new0 = m00*a0 + m01*a1
new1 = m10*a0 + m11*a1
```

### Gates do laboratório

| Gate | Matriz | Efeito em |0> | Efeito em |1> |
|------|--------|-------------|-------------|
| X    | [[0,1],[1,0]] | |1> | |0> |
| Z    | [[1,0],[0,-1]] | |0> | -|1> |
| H    | 1/√2 [[1,1],[1,-1]] | superposição | superposição |

## 4. Pareamento de índices

`bit = 1<<qubit`. Percorremos blocos de `step=2*bit`; dentro de cada bloco pareamos índice com bit 0 e o parceiro com bit 1.

```text
2 qubits, qubit alvo = 1 (bit=2, step=4)

índices:  0   1   2   3
bits:    00  01  10  11
pares:   (0,2) e (1,3)  -- diferem no bit 1
```

### Trace manual — H no qubit 0 de |00>

Estado inicial `[1,0,0,0]`. Após H em qubit 0:

```text
par (0,2): a0=1,a1=0 -> (1/√2, 1/√2) nos índices 0 e 2
par (1,3): a0=0,a1=0 -> permanece zero
resultado: [1/√2, 0, 1/√2, 0]
```

## 5. CNOT

Só troca amplitudes quando control=1 e target=0, evitando fazer o swap duas vezes.

```text
control=0, target=1
|10> <-> |11>  (troca quando control bit set e target bit clear no índice menor)
```

Para Bell: H(0) depois CNOT(0,1) produz `(|00> + |11>)/√2`.

## 6. Invariantes

| Invariante | Checagem |
|------------|----------|
| norma unitária | soma |amp|² = 1 após gates unitários |
| `state_.size() == 2^n` | construtor valida qubits |
| qubit em `[0, n)` | `check_qubit` |
| control ≠ target em CNOT | erro explícito |
| gates unitários preservam norma | testes de probabilidade |

## 7. Bugs clássicos

1. **Sobrescrever `a0` antes de calcular `a1`** no par de amplitudes.
2. **Trocar CNOT duas vezes no mesmo par** (swap duplo cancela).
3. **H sem normalização 1/√2**.
4. **Confundir ordem de bits** entre little-endian de índice e convenção do desenho.
5. **Aplicar gate 2-qubit como dois 1-qubit independentes** (errado para CNOT).

## 8. Comparação com produção

| Aspecto | Este lab | Qiskit/Cirq | Hardware real |
|---------|----------|-------------|---------------|
| Representação | state vector denso | múltiplos backends | qubits físicos |
| Limite prático | ~20-24 qubits RAM | sim + otimizações | ruído, decoerência |
| Gates | X,H,Z,CNOT | biblioteca ampla | nativos + calibração |
| Medição | probabilidade | amostragem | shots |

Simuladores industriais usam representação esparsa, tensor network ou GPU para certos circuitos. O pareamento por bitmask que você implementa é o núcleo de muitos kernels CPU.

## 9. Diagrama do circuito Bell

```text
q0: --H--*--
         |
q1: -----X--
```

Estado final: 50% |00>, 50% |11>, 0% |01> e |10>.

## 10. Probabilidade e medição (conceito)

Probabilidade do basis state `|i>` é `|state_[i]|²`. O teste Bell verifica P(00)=P(11)=0.5. Medições reais colapsam o estado; nosso simulador pode apenas reportar probabilidades sem colapsar, dependendo do teste.

## 11. Complexidade

Aplicar gate 1-qubit: O(2^n). CNOT na implementação ingênua: O(2^n). Circuito com g gates: O(g * 2^n). Por isso simulação clássica explode.

## 12. Exemplo completo 2-qubit

```text
início: |00>
H(0):   (|00> + |10>)/√2
CNOT(0,1): (|00> + |11>)/√2
P(00)=0.5, P(11)=0.5
```

## 13. Perguntas de verificação

1. Quantos bytes para 10 qubits?
2. Por que copiamos `a0` e `a1` antes de escrever de volta?
3. Qual índice representa |11> em nosso layout?

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
