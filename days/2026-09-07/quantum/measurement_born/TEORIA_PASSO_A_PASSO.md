# Teoria — measurement & Born rule

Continuação de `days/2026-09-04/quantum/statevector_intro`. TODOs: `Q-MEAS-01`, `Q-MEAS-02`, `Q-BORN-03`.

## 1. Statevector 2-qubit

Quatro amplitudes complexas `|00⟩,|01⟩,|10⟩,|11⟩`. Norma deve ser 1.

## 2. Porta H em q0

Superposição igual entre paridades de q0 — após H, P(0)=P(1)=0.5 para qubit medido.

## 3. Regra de Born (Q-MEAS-01)

P(i) = |a_i|². Implementação delega a `probability(index)`.

## 4. Colapso (Q-MEAS-02)

Medição projeta na base computacional — estado vira delta em `index`.

## 5. born_select (Q-BORN-03)

Inverse CDF com u determinístico para testes — `u=0.25` em {0.5,0.5} escolhe índice 1.

## 6. Trace — |0⟩ + H

```text
|ψ⟩ = |0⟩
H q0 → (|00⟩+|10⟩+|01⟩+|11⟩)/2  (simplificado no lab 2-qubit)
P(|00⟩) = 0.5
```

## 7. Por quê simular medição?

Hardware real é estocástico; testes precisam de RNG seed ou u fixo.

## 8. Ligação com qsim capstone

Portar para `projects/chris-qsim` após passar `measure_tests`.

## 9. Invariantes

- Σ P(i) = 1 após gates unitários.
- Após colapso, norma 1 na base escolhida.

## 10. Bugs comuns

- Esquecer normalização após colapso parcial.
- Confundir índice linear com (q0,q1).

## 11. Comparação

| Lab | Qiskit |
|-----|--------|
| statevector manual | simulador otimizado |

## 12. Complexidade

O(2^n) — aqui n=2 é trivial.

## 13. Medição vs gate

Gates são unitários reversíveis; medição é não-unitária.

## 14. Por quê C++?

Mesma stack do Day 04 — sem mudar linguagem no meio da trilha quantum.

## 15. Síntese

### Por quê três TODOs?

Medir probabilidade, colapsar e amostrar são operações distintas em simuladores reais.

### Por quê após statevector_intro?

Você já aplica H/X/Z/CNOT — agora interpreta resultados estatísticos.

### Por quê u determinístico?

Reprodutibilidade em `ctest` sem mock de RNG global.

## 16. Exercício mental

Calcule P(1) após H em |0⟩ de 1 qubit — deve ser 0.5.

## 17. Próximo passo

Ruído e decoerência ficam fora do escopo — ver roadmap qsim.

## 18. Diagrama

```text
|ψ⟩ --H-- measure -- collapse --> |i⟩
```

## 19. Notação

`|a+bi|² = a²+b²` para amplitude complexa.

## 20. Fechamento

Este lab fecha o arco “introdução quântica” do portfólio antes de capstones.

## 21. Paper-trace

Calcule P(0) após H em |0⟩ de 1 qubit — 0.5.

## 22. Gate

`ctest` no módulo `measurement_born`.

## 23. Ordem no dia

Após bloco drivers; pode ser paralelo ao bloco AI.

## 24. Normalização global

Este lab não renormaliza após H — assume amplitudes já corretas do gate.

## 25. Leitura obrigatória

Revise `statevector_intro` TEORIA §Bell antes de medir.

