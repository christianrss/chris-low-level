# Teoria passo a passo — phase kickback (2 qubits)

Laboratório em **C++**. Estado `|b1 b0>` em vetor amp[4]: índices 0=00,1=01,2=10,3=11.

## 1. O quê

CZ control=q0 target=q1 multiplica amp[3] por -1. Phase kickback: fase no target controlado aparece no controle em superposição.

## 2. Trace

```text
reset → (1,0,0,0)
H0 → (1/√2, 0, 1/√2, 0)  P(00)=P(10)=0.5
|11> = (0,0,0,1); CZ → (0,0,0,-1)
```

## 3. Por quê -1 só em |11>

CZ = diag(1,1,1,-1) na base computacional.

## 4. Por quê kickback

Com controle em |+| e target |1|, a fase relativa distingue ramos do controle.

## 5. Invariantes

- ||amp||^2 = 1 após H
- CZ é unitária (só muda sinal)

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| flip amp[2] | qubit order errado |
| P≠0.5 | H mal implementado |

## 7. Checklist

- [ ] P=0.5 após H
- [ ] amp[3] negativo após CZ em |11>

## Caderno de verificação — phase_kickback

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. |00> reset.
2. H → 0.5.
3. CZ flip |11>.
4. Índice 3.
5. Norma 1.

## Tabela de papéis

| Papel | Neste lab |
|-------|-----------|
| Entrada | fixture / buffer do Caso 1 |
| Transformação | corpo do TODO |
| Saída | valor comparado no assert |
| Erro | retorno negativo / false / Err |

## Fluxo

```text
fixture → bounds check → transformação → assert do teste
```

## Por quê falhar cedo

Erro de formato deve aparecer no retorno, não como valor default silencioso.

## Por quê o assert usa número fixo

O número fixo congela o contrato pedagógico; mudar o teste esconde o bug.

## Por quê não delegar ao gabarito

A RESOLUCAO traz o código completo; tente no starter antes de abrir solutions.

## Checklist final da teoria

- [ ] Trace do Caso 1 no papel
- [ ] Sei arquivo e função de cada TODO
- [ ] Sei o valor exato que o assert compara

- Item de revisão 85: confirme o offset/valor do Caso 1 outra vez (revisão -15).
- Item de revisão 86: confirme o offset/valor do Caso 1 outra vez (revisão -14).
- Item de revisão 87: confirme o offset/valor do Caso 1 outra vez (revisão -13).
- Item de revisão 88: confirme o offset/valor do Caso 1 outra vez (revisão -12).
- Item de revisão 89: confirme o offset/valor do Caso 1 outra vez (revisão -11).
- Item de revisão 90: confirme o offset/valor do Caso 1 outra vez (revisão -10).
- Item de revisão 91: confirme o offset/valor do Caso 1 outra vez (revisão -9).
- Item de revisão 92: confirme o offset/valor do Caso 1 outra vez (revisão -8).
- Item de revisão 93: confirme o offset/valor do Caso 1 outra vez (revisão -7).
- Item de revisão 94: confirme o offset/valor do Caso 1 outra vez (revisão -6).
- Item de revisão 95: confirme o offset/valor do Caso 1 outra vez (revisão -5).
- Item de revisão 96: confirme o offset/valor do Caso 1 outra vez (revisão -4).
- Item de revisão 97: confirme o offset/valor do Caso 1 outra vez (revisão -3).
- Item de revisão 98: confirme o offset/valor do Caso 1 outra vez (revisão -2).
- Item de revisão 99: confirme o offset/valor do Caso 1 outra vez (revisão -1).
- Item de revisão 100: confirme o offset/valor do Caso 1 outra vez (revisão 0).
- Item de revisão 101: confirme o offset/valor do Caso 1 outra vez (revisão 1).
- Item de revisão 102: confirme o offset/valor do Caso 1 outra vez (revisão 2).
- Item de revisão 103: confirme o offset/valor do Caso 1 outra vez (revisão 3).
- Item de revisão 104: confirme o offset/valor do Caso 1 outra vez (revisão 4).
- Item de revisão 105: confirme o offset/valor do Caso 1 outra vez (revisão 5).
- Item de revisão 106: confirme o offset/valor do Caso 1 outra vez (revisão 6).
- Item de revisão 107: confirme o offset/valor do Caso 1 outra vez (revisão 7).
- Item de revisão 108: confirme o offset/valor do Caso 1 outra vez (revisão 8).
- Item de revisão 109: confirme o offset/valor do Caso 1 outra vez (revisão 9).
- Item de revisão 110: confirme o offset/valor do Caso 1 outra vez (revisão 10).
- Item de revisão 111: confirme o offset/valor do Caso 1 outra vez (revisão 11).
- Item de revisão 112: confirme o offset/valor do Caso 1 outra vez (revisão 12).
- Item de revisão 113: confirme o offset/valor do Caso 1 outra vez (revisão 13).
- Item de revisão 114: confirme o offset/valor do Caso 1 outra vez (revisão 14).
- Item de revisão 115: confirme o offset/valor do Caso 1 outra vez (revisão 15).
- Item de revisão 116: confirme o offset/valor do Caso 1 outra vez (revisão 16).
- Item de revisão 117: confirme o offset/valor do Caso 1 outra vez (revisão 17).
- Item de revisão 118: confirme o offset/valor do Caso 1 outra vez (revisão 18).
- Item de revisão 119: confirme o offset/valor do Caso 1 outra vez (revisão 19).
- Item de revisão 120: confirme o offset/valor do Caso 1 outra vez (revisão 20).
- Item de revisão 121: confirme o offset/valor do Caso 1 outra vez (revisão 21).
- Item de revisão 122: confirme o offset/valor do Caso 1 outra vez (revisão 22).
- Item de revisão 123: confirme o offset/valor do Caso 1 outra vez (revisão 23).
- Item de revisão 124: confirme o offset/valor do Caso 1 outra vez (revisão 24).
