# Resolução guiada — measurement_born

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função | Substituir |
|---------|-----------------|--------|------------|
| `Q-MEAS-01` | `starter/src/measure.cpp` | `measure_probability` | stub TODO |
| `Q-MEAS-02` | `starter/src/measure.cpp` | `collapse_to` | stub TODO |
| `Q-BORN-03` | `starter/src/measure.cpp` | `born_select` | stub TODO |

## Baseline

```powershell
cd days/2026-09-07/quantum/measurement_born/starter
cmake -S . -B build_ci && cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL até implementar medição/colapso/Born.

## Relatório de resolução

## Q-MEAS-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/measure.cpp` |
| Função | `measure_probability` |

### 1. O problema

Probabilidade de medir `|index⟩` é `|a_index|²` (regra de Born).

### Escreva o código

```cpp
double StateVector2::measure_probability(std::size_t index) const {
    return probability(index);
}
```

### Por que funciona?

`probability` já calcula `std::norm` da amplitude.

### Verifique

Caso 1: após H em q0, P(0)=P(1)=0.5.

### Debug

| Sintoma | Ação |
|---------|------|
| P > 1 | verificar normalização |

---

## Q-MEAS-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/measure.cpp` |
| Função | `collapse_to` |

### 1. O problema

Após medição o estado deve colapsar na base computacional.

### Escreva o código

```cpp
void StateVector2::collapse_to(std::size_t index) {
    for (std::size_t i = 0; i < state_.size(); ++i) {
        state_[i] = (i == index) ? std::complex<double>{1.0, 0.0}
                                 : std::complex<double>{0.0, 0.0};
    }
}
```

### Por que funciona?

Post-measurement state é ortonormal na base escolhida.

### Verifique

Caso 2: `probability(1) == 1` após `collapse_to(1)`.

---

## Q-BORN-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/measure.cpp` |
| Função | `born_select` |

### 1. O problema

Testes precisam de amostragem determinística via `u` uniforme.

### Escreva o código

```cpp
std::size_t StateVector2::born_select(const std::vector<double>& probs, double u) {
    double acc = 0.0;
    for (std::size_t i = 0; i < probs.size(); ++i) {
        acc += probs[i];
        if (u < acc) return i;
    }
    return probs.empty() ? 0 : probs.size() - 1;
}
```

### Por que funciona?

Inverse CDF — acumula probabilidades até ultrapassar `u`.

### Verifique

Caso 3: `born_select({0.5,0.5}, 0.25) == 1`.

### Resultado esperado

`ctest` passa `measure_tests`.
