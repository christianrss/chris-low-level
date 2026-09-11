# Teoria passo a passo — estado de Bell em C++

Este laboratório é em **C++**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

O lab de medição do Dia 07 assume um estado pronto. Aqui você **prepara** `|Φ+⟩ = (|00⟩+|11⟩)/√2` com H no qubit 0 e CNOT.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

Indexação |q1 q0|: índice = q1*2+q0.
| bits | índice | |00⟩ inicial |
|------|--------|-------------|
| 00 | 0 | 1 |
| 01 | 1 | 0 |
| 10 | 2 | 0 |
| 11 | 3 | 0 |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
reset: [1, 0, 0, 0]
H no q0 (mistura índices 0 com 2, 1 com 3):
  a0' = (a0+a2)/√2 = 1/√2 ≈ 0.707106781
  a2' = (a0-a2)/√2 = 1/√2
  a1' = a3' = 0
CNOT (controle q0, alvo q1) troca amp[2] com amp[3]:
  [1/√2, 0, 0, 1/√2]
P(00)=0.5, P(11)=0.5, P(01)=0
```

## Algoritmo (ordem obrigatória)

1. q_reset põe amp[0]=1 e o resto 0.
2. q_h0 aplica Hadamard no qubit 0 sobre o vetor de 4 componentes (sem matriz 4x4 explícita).
3. q_cnot troca amp[2] e amp[3] (os estados em que q0=1).
4. q_prob é o quadrado da amplitude (estado real).

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Esquecer de zerar amp[1..3]: o teste de |00⟩ falha.
- H sem 1/√2: a amplitude não é ~0.707.
- CNOT trocar 0 com 1: P(11) não vira 0.5.

## Lab versus produção

Qiskit `H(0); CX(0,1)` produz o mesmo vetor. Aqui não há fase imaginária.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `quantum/bell_state_prep`, o fluxo de dados não é abstrato: cada função do starter
transforma um buffer ou um estado finito e devolve um valor que o teste compara
com igualdade estrita.

```text
entrada (fixture / literal do teste)
    → validação de limites (OOB / estado ilegal)
    → transformação (decode / fold / push / parse)
    → saída (string, código, ponteiro, probabilidade)
```

Por quê essa ordem? Se a validação vier depois da transformação, um buffer curto
gera leitura lixo e o assert falha com um número “quase certo”, difícil de depurar.

## Estruturas e papéis

| Peça | Papel | O que o teste fixa |
|------|-------|--------------------|
| buffer / stream | memória linear | bytes literais no caso |
| cursor / pc / head | progresso | avanço exatamente do size |
| estado / flags | FSM ou capacidade | transição ilegal rejeitada |
| retorno de erro | falha explícita | -1 / Err / false / throw |

## Trace estendido (mesmo caso, mais colunas)

Reescreva o Caso 1 da TEORIA com quatro colunas no papel:

```text
passo | cursor | lê | produz
------+--------+----+--------
(use os números já listados acima; não invente outro exemplo)
```

Se o cursor após o passo N não for o início do passo N+1, o listing ou o anel
desalinha e a string/valor diverge do assert.

## Invariantes reforçadas

1. Mesma entrada → mesma saída (determinismo).
2. Erro de formato não vira valor default silencioso.
3. Capacidade / size / transição ilegal falha **agora**.
4. O arquivo editado é só o citado na RESOLUCAO; o teste não se altera.

## Depuração dirigida

| Sintoma no teste | Hipótese #1 | O que imprimir |
|------------------|-------------|----------------|
| string/valor off-by-one | endianness ou size | hex do buffer e cursor |
| falha só no 2º caso | estado residual | reset entre casos |
| passe local, falha no runner | cwd / fixture path | path absoluto do fixture |

## Comparação com produção (detalhe)

Em ferramentas reais o mesmo contrato aparece com outros nomes: `objdump` (size
por opcode), `epoll` (anel de eventos), `softmax` em kernels CUDA (max-subtract).
Aqui o recorte é pequeno o bastante para caber no papel e grande o bastante para
o assert rejeitar o bug clássico.

## Trecho âncora do gabarito (só para conferir assinaturas)

Não copie cegamente. Use para confirmar nomes de funções e constantes:

```text
#include "bell.hpp"
#include <math.h>
void q_reset(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-01
    amp[0] = 1.0; amp[1] = 0.0; amp[2] = 0.0; amp[3] = 0.0;
}
void q_h0(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-02
    const double s = 1.0 / sqrt(2.0);
    double a0 = amp[0], a1 = amp[1], a2 = amp[2], a3 = amp[3];
    amp[0] = s * (a0 + a2);
    amp[1] = s * (a1 + a3);
    amp[2] = s * (a0 - a2);
    amp[3] = s * (a1 - a3);
}
void q_cnot(double amp[4]) {
    // PEDAGOGY-SOLUTION: Q-BELL-03
    double a2 = amp[2], a3 = amp[3];
    amp[2] = a3;
    amp[3] = a2;
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
```

## Base |00⟩ → Bell |Φ+⟩

Amplitudes `[a00, a01, a10, a11]` = índices 0..3.

```text
reset: [1, 0, 0, 0]          P(00)=1
H no qubit 0:
  s = 1/sqrt(2) ≈ 0.70710678
  [s, 0, s, 0]               P(00)=P(10)=0.5
CNOT (control 0, target 1):
  troca a10 ↔ a11
  [s, 0, 0, s]               P(00)=P(11)=0.5
```

**Por quê** H antes de CNOT? Sem H, CNOT em |00⟩ não cria entrelaçamento.

## Fórmulas

```text
H0:  a0' = s(a0+a2); a1' = s(a1+a3);
     a2' = s(a0-a2); a3' = s(a1-a3);
CNOT: (a2, a3) ← (a3, a2)
P(k) = amp[k]^2
```

## Invariantes

- Σ P(k) = 1 (norma preservada sob unitárias)
- Após Bell: P(01)=P(10)=0
- reset sempre |00⟩

## Bugs comuns

- Aplicar H no qubit errado (índices)
- CNOT sem temporários → overwrite
- Comparar amplitudes com `==` float em vez de probs

## Lab vs produção

Qiskit/Cirq usam matrizes 4×4; aqui você aplica o efeito na mão
para ver o vetor mudar — base do módulo measurement (Dia 07).

## Checklist

- [ ] reset → [1,0,0,0]
- [ ] após H+CNOT: P(00)=P(11)=0.5
- [ ] s = 1/√2 no papel
