# Resolução guiada — phase_kickback

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `Q-PHASE-01` | `starter/phase.cpp` | `q_reset` |
| `Q-PHASE-02` | `starter/phase.cpp` | `q_h0` |
| `Q-PHASE-03` | `starter/phase.cpp` | `q_cz` |

## Baseline

```powershell
cd days/2026-09-11/quantum/phase_kickback/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.

## Q-PHASE-01

### Onde colocar (Q-PHASE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/phase.cpp` |
| Função | `q_reset` |
| Substituir | o corpo sob o comentário `TODO [Q-PHASE-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Estado |00>.

### Algoritmo / trace

amp[0]=1 demais 0.

### Escreva o código

```cpp
    amp[0]=1.0;
    amp[1]=0.0;
    amp[2]=0.0;
    amp[3]=0.0;
```

### Por que funciona?

Base computacional.

### Verifique

amp[0]==1.

### Código completo alinhado ao solutions/ (Q-PHASE-01)

```cpp
PEDAGOGY-SOLUTION: Q-PHASE-01 */
    amp[0]=1; amp[1]=0; amp[2]=0; amp[3]=0;
}
void q_h0(double amp[4]) {
    /* 
```

## Q-PHASE-02

### Onde colocar (Q-PHASE-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/phase.cpp` |
| Função | `q_h0` |
| Substituir | o corpo sob o comentário `TODO [Q-PHASE-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

P(00)=P(10)=0.5.

### Algoritmo / trace

Hadamard no qubit 0 (mesmo mapa do Bell lab).

### Escreva o código

```cpp
    const double s = 1.0/std::sqrt(2.0);
    double a0=amp[0], a1=amp[1], a2=amp[2], a3=amp[3];
    amp[0]=s*(a0+a2); amp[1]=s*(a1+a3);
    amp[2]=s*(a0-a2); amp[3]=s*(a1-a3);
```

### Por que funciona?

Mistura |0*> e |1*> do controle.

### Verifique

probs 0.5.

### Código completo alinhado ao solutions/ (Q-PHASE-02)

```cpp
PEDAGOGY-SOLUTION: Q-PHASE-02 */
    const double s = 1.0/std::sqrt(2.0);
    double a0=amp[0], a1=amp[1], a2=amp[2], a3=amp[3];
    amp[0]=s*(a0+a2); amp[1]=s*(a1+a3); amp[2]=s*(a0-a2); amp[3]=s*(a1-a3);
}
void q_cz(double amp[4]) {
    /* 
```

## Q-PHASE-03

### Onde colocar (Q-PHASE-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/phase.cpp` |
| Função | `q_cz` |
| Substituir | o corpo sob o comentário `TODO [Q-PHASE-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Sinal de |11> deve inverter.

### Algoritmo / trace

amp[3] = -amp[3].

### Escreva o código

```cpp
    amp[3] = -amp[3];
    /* CZ diag */
    /* done */
```

### Por que funciona?

Única entrada -1 no CZ.

### Verifique

amp[3]<0 partindo de +1.

### Código completo alinhado ao solutions/ (Q-PHASE-03)

```cpp
PEDAGOGY-SOLUTION: Q-PHASE-03 */
    amp[3] = -amp[3];
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| índice 2 | use 3 para |11> |

## Relatório de resolução

- TODOs: [ ]
