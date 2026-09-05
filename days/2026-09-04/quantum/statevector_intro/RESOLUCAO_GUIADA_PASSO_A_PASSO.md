# Resolução guiada passo a passo — State-vector simulator

## Mapa exato starter → resolução

- `D2-QSIM-SINGLE` → `starter/src/qsim.cpp`
- `D2-QSIM-X` → `starter/src/qsim.cpp`
- `D2-QSIM-H` → `starter/src/qsim.cpp`
- `D2-QSIM-Z` → `starter/src/qsim.cpp`
- `D2-QSIM-CNOT` → `starter/src/qsim.cpp`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

## Baseline

```bash
cmake -S days/2026-09-04/quantum/statevector_intro/starter -B days/2026-09-04/quantum/statevector_intro/starter/build
cmake --build days/2026-09-04/quantum/statevector_intro/starter/build
ctest --test-dir days/2026-09-04/quantum/statevector_intro/starter/build --output-on-failure
```

## Fácil — kernel de gate 1-qubit
Abra `starter/src/qsim.cpp`, função `apply_single`.

Valide o qubit:

```cpp
check_qubit(qubit);
```

Calcule máscara e passo:

```cpp
const std::size_t bit = std::size_t{1} << qubit;
const std::size_t step = bit << 1;
```

Agora percorra pares:

```cpp
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

Use cópias `a0/a1`; se sobrescrever `state_[zero]` antes de salvar `a0`, o cálculo de `state_[one]` usará dado já modificado.

### Por que funciona?
`bit` isola o qubit alvo; `step = 2*bit` agrupa pares `(|0⟩,|1⟩)` que compartilham todos os outros bits. O loop 2×2 aplica a matriz sem misturar pares de qubits diferentes. Cópias `a0/a1` evitam ler amplitude já atualizada.

## Médio — X, H e Z
X:

```cpp
apply_single(qubit, {0, 0}, {1, 0}, {1, 0}, {0, 0});
```

H:

```cpp
const double s = 1.0 / std::sqrt(2.0);
apply_single(qubit, {s, 0}, {s, 0}, {s, 0}, {-s, 0});
```

Z:

```cpp
apply_single(qubit, {1, 0}, {0, 0}, {0, 0}, {-1, 0});
```

Depois de H em |0>, confira manualmente que probabilidades são 0.5/0.5 e norma 1.

### Por que funciona?
X troca amplitudes |0⟩↔|1⟩; H cria superposição com coeficientes `1/√2`; Z aplica fase −1 em |1⟩. Todos delegam ao mesmo `apply_single` — uma implementação, várias portas.

## Difícil — CNOT
Comece:

```cpp
check_qubit(control);
check_qubit(target);
if (control == target) {
    throw std::invalid_argument("control and target must differ");
}
```

Máscaras:

```cpp
const std::size_t control_bit = std::size_t{1} << control;
const std::size_t target_bit = std::size_t{1} << target;
```

Percorra índices e troque somente o representante com target=0:

```cpp
for (std::size_t index = 0; index < state_.size(); ++index) {
    const bool control_on = (index & control_bit) != 0;
    const bool target_off = (index & target_bit) == 0;
    if (control_on && target_off) {
        const std::size_t partner = index | target_bit;
        std::swap(state_[index], state_[partner]);
    }
}
```

### Por que funciona?
CNOT flipa target somente quando control está 1. `index | target_bit` é o parceiro com target invertido; trocar uma vez por par evita double-swap. Condição `target_off` garante processar cada par uma única vez.

## Teste Bell
O teste executa:

```cpp
StateVector bell(2);
bell.apply_h(0);
bell.apply_cnot(0, 1);
```

Esperado neste layout de bits:

```text
P(00)=0.5
P(11)=0.5
P(01)=0
P(10)=0
norm=1
```

## Debug
Se norma sair de 1 após H, inspecione `s`, `a0`, `a1`, `zero`, `one`. Se Bell aparecer em índices errados, desenhe os bits binários dos índices 0..3 e aplique as máscaras manualmente.

## Benchmark

```bash
cmake -S days/2026-09-04/quantum/statevector_intro/starter -B days/2026-09-04/quantum/statevector_intro/starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build days/2026-09-04/quantum/statevector_intro/starter/build-bench
./days/2026-09-04/quantum/statevector_intro/starter/build-bench/chris_qsim_benchmark
```

Registre `qubits`, `amplitudes`, `bytes`, `gates/s` e `norm`. Verifique empiricamente que cada qubit adicional dobra amplitudes/memória.


## Solução final comentada
Depois de deixar o starter verde, compare somente os blocos `PEDAGOGY-SOLUTION` em `solutions/` correspondentes aos IDs do mapa. Se houver uma linha necessária no gabarito que não foi ensinada acima, trate como defeito do material e não como algo que você deveria adivinhar.

## Relatório de resolução

| ID | Gate | Critério |
|----|------|----------|
| D2-QSIM-SINGLE | kernel 2x2 | cópias `a0`/`a1` antes de escrever |
| D2-QSIM-X/H/Z | Pauli/H | H usa `1/sqrt(2)` |
| D2-QSIM-CNOT | entrelaçamento | swap único quando control=1, target=0 |

Aceite: teste Bell com P(00)=P(11)=0.5 e norma 1. Se norma diverge após H, inspecione constante `s`. Benchmark deve mostrar crescimento ~2^n em memória e tempo por gate.
