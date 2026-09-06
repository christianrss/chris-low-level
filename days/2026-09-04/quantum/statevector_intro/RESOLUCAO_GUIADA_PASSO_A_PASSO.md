# RESOLUÇÃO GUIADA — Quantum / State-vector intro

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D2-QSIM-SINGLE` | `starter/src/qsim.cpp` | `apply_single` |
| `D2-QSIM-X` | `starter/src/qsim.cpp` | `apply_x` |
| `D2-QSIM-H` | `starter/src/qsim.cpp` | `apply_h` |
| `D2-QSIM-Z` | `starter/src/qsim.cpp` | `apply_z` |
| `D2-QSIM-CNOT` | `starter/src/qsim.cpp` | `apply_cnot` |

Cada ID: `TODO` / `PEDAGOGY-SOLUTION` / `PEDAGOGY-TEST`. Se não bater, pare.

> Trabalhe em `days/2026-09-04/quantum/statevector_intro/starter/`.

Assinatura do kernel: `apply_single(qubit, m00, m01, m10, m11)` — quatro `complex<double>`.

---

## Baseline

```bash
cmake -S starter -B starter/build && cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

`StateVector` já expõe `amplitude` / `probability` / `norm_squared` — use-os na verificação; não reimplemente norma nos TODOs. Ordem: SINGLE → X/H/Z → CNOT.

---

## Exercício Fácil — `D2-QSIM-SINGLE`

### 1. O problema

TODO vazio: nenhum gate muda o estado. X/H/Z/CNOT dependem deste kernel.

### 2. O algoritmo

```text
check_qubit(qubit)
bit = 1 << qubit;  step = bit << 1
para base = 0..size step step:
  para offset = 0..bit-1:
    zero = base+offset; one = zero+bit
    a0,a1 = state[zero], state[one]   # cópias!
    state[zero] = m00*a0 + m01*a1
    state[one]  = m10*a0 + m11*a1
```

### 3. Escreva o código

```cpp
check_qubit(qubit);
const std::size_t bit = std::size_t{1} << qubit;
const std::size_t step = bit << 1;
for (std::size_t base = 0; base < state_.size(); base += step) {
    for (std::size_t offset = 0; offset < bit; ++offset) {
        const std::size_t zero = base + offset;
        const std::size_t one = zero + bit;
        const auto a0 = state_[zero];
        const auto a1 = state_[one];
        state_[zero] = m00 * a0 + m01 * a1;
        state_[one] = m10 * a0 + m11 * a1;
    }
}
```

### 4. Por que funciona

`bit` isola o qubit; `step=2*bit` agrupa pares que compartilham os outros bits. Cópias evitam ler amplitude já atualizada.

Exemplo 3 qubits, alvo=1 (`bit=2`, `step=4`): bases `0,4,…`; em cada base offsets `0,1` geram pares `(0,2),(1,3)`, depois `(4,6),(5,7)`, …

Sem `check_qubit`, um índice `>= n` lê fora de `state_` — UB.

### 5. Verifique

Ainda sem wrappers; compile e siga para X/H/Z. Não rode o suite Bell até H e CNOT existirem.

---

## Exercício Médio — wrappers `X` / `H` / `Z`

Três TODOs, um kernel. Implemente na ordem X → H → Z e confira norma após H antes do CNOT.

### `D2-QSIM-X`

#### 1. O problema
Starter vazio — X não altera o estado.

#### 2–3. Algoritmo e código
Matriz X = `[[0,1],[1,0]]`:

```cpp
apply_single(qubit, {0, 0}, {1, 0}, {1, 0}, {0, 0});
```

#### 4–5. Por que / verifique
Troca \|0⟩↔\|1⟩ do qubit alvo. Em 1 qubit: estado `[1,0]` → `[0,1]`.

### `D2-QSIM-H`

#### 1. O problema
Sem H normalizado, Bell e probs falham.

#### 2–3. Algoritmo e código

```cpp
const double s = 1.0 / std::sqrt(2.0);
apply_single(qubit, {s, 0}, {s, 0}, {s, 0}, {-s, 0});
```

Matriz: `[[s,s],[s,-s]]`. Não omita o `-s`.

#### 4–5. Por que / verifique
Após H em \|0⟩: P(0)=P(1)=0.5 e `norm_squared()≈1`. Se norma ≠ 1, revise `s` e as cópias em `apply_single`.

### `D2-QSIM-Z`

#### 1. O problema
Z vazio; fase em \|1⟩ não aplicada.

#### 2–3. Código

```cpp
apply_single(qubit, {1, 0}, {0, 0}, {0, 0}, {-1, 0});
```

#### 4–5. Por que / verifique
Fase −1 em \|1⟩; probs iguais, mas interferência muda em circuitos maiores. Um kernel, três portas — não copie o loop de pareamento.

---

## Exercício Difícil — `D2-QSIM-CNOT`

### 1. O problema

Sem CNOT não há Bell. Starter ignora control/target.

### 2. O algoritmo

```text
check control e target; se iguais → invalid_argument
control_bit = 1<<control; target_bit = 1<<target
para cada index:
  se (index & control_bit) e !(index & target_bit):
    swap(state[index], state[index | target_bit])
```

### 3. Escreva o código

```cpp
check_qubit(control);
check_qubit(target);
if (control == target) {
    throw std::invalid_argument("control and target must differ");
}
const std::size_t control_bit = std::size_t{1} << control;
const std::size_t target_bit = std::size_t{1} << target;
for (std::size_t index = 0; index < state_.size(); ++index) {
    const bool control_on = (index & control_bit) != 0;
    const bool target_off = (index & target_bit) == 0;
    if (control_on && target_off) {
        const std::size_t partner = index | target_bit;
        std::swap(state_[index], state_[partner]);
    }
}
```

### 4. Por que funciona

Flip do target só com control=1. `target_off` processa cada par uma vez — sem double-swap.

Para 2 qubits, control=0, target=1: índices com bit0=1 e bit1=0 são `01` (index 1). Partner `01|10` = `11` (index 3). Troca amplitudes de `|01⟩` e `|11⟩` — mas no estado pós-H(0) só `|00⟩` e `|10⟩` têm massa, então o swap relevante é em outro par… Trace Bell completo está no checkpoint abaixo; desenhe os quatro índices antes de depurar no debugger.

### 5. Verifique

```cpp
StateVector bell(2);
bell.apply_h(0);
bell.apply_cnot(0, 1);
// P(00)=P(11)=0.5, P(01)=P(10)=0, norm=1
```

```bash
ctest --test-dir starter/build --output-on-failure
```

Se P(10)=0.5 e P(11)=0, você provavelmente inverteu control/target ou a convenção de bit.
---

## Checkpoint no papel — Bell em 4 amplitudes

Índices (qubit0 = bit menos significativo neste layout de máscara):

```text
index  bits(q1 q0)   após H(0)        após CNOT(0,1)
0      00            1/√2             1/√2
1      01            0                0
2      10            1/√2             0
3      11            0                1/√2
```

Se após CNOT você tiver massa em `|10⟩` em vez de `|11⟩`, control/target estão trocados ou a condição `target_off` falhou.

Trace de um par em `apply_single` (qubit 0, 2 qubits): pares `(0,1)` e `(2,3)` — diferem só no bit 0.

## Debugging

- Norma ≠ 1 após H → constante `s`, cópias `a0/a1`, escrita in-place sem salvar.
- Bell em índices errados → tabela acima + máscaras `1<<q`.
- CNOT no-op → falta `target_off` (swap duplo cancela) ou bits trocados.
- `invalid_argument` esperado se `control == target`.

## Benchmark

```bash
cmake -S starter -B starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build starter/build-bench
./starter/build-bench/chris_qsim_benchmark
```

Registre qubits, amplitudes, bytes, gates/s, norm. Cada qubit adicional **dobra** amplitudes/memória — confirme empiricamente.

## Mapa de consistência

Compare `PEDAGOGY-SOLUTION` em `solutions/src/qsim.cpp` só depois do starter verde.

## Relatório

| ID | Critério |
|----|----------|
| SINGLE | cópias antes de escrever |
| X/H/Z | H com `1/sqrt(2)` |
| CNOT | swap único control=1, target=0 |

Aceite: Bell P(00)=P(11)=0.5 e norma 1. Próximo: anote em `BENCHMARK_GUIADO.md` o ponto onde RAM/gates/s ficam inviáveis na sua máquina.

## Exemplo trabalhado — 1 qubit, sequência HZH

No papel (opcional, reforço):

```text
|0⟩ --H--> (|0⟩+|1⟩)/√2 --Z--> (|0⟩-|1⟩)/√2 --H--> |1⟩
```

Se Z ou H estiver errada, o estado final não será \|1⟩. Isso separa bugs de fase (Z) de bugs de normalização (H) sem precisar de CNOT.

Lembrete de API: `apply_single(qubit, m00, m01, m10, m11)` — ordem row-major da matriz 2×2. Confunda `m01` com `m10` e X/H quebram de formas diferentes (X deixa de ser involução).

Construtor já garante `1 ≤ qubits ≤ 24` e estado `|00…0⟩`. Não reinsira essa lógica nos TODOs — só use `check_qubit` / guards de CNOT.

Depois do verde: compare marcadores `PEDAGOGY-SOLUTION` em `solutions/src/qsim.cpp`. Registre no benchmark o maior `n` de qubits que ainda roda confortável na sua máquina — esse número é o “orçamento clássico” do simulador.

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Paper-trace feito? Sim/Não
- Portei para projects/? Sim/Não — evidência: ___
