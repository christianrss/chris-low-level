# Teoria passo a passo — SharedArrayBuffer ring CAP 4

Laboratório em **JavaScript**. Ring de capacidade 4 com `Atomics` em Int32Array.

## 1. Layout

```text
view[0]=head, view[1]=tail, view[2..5]=slots
```

## 2. Trace

```text
push 10,20,30,40 → size 4; push 50 → false
pop → 10, depois 20; size → 2
```

## 3. Por quê Atomics

Workers compartilham SAB; load/store atômicos evitam tear em índices.

## 4. Por quê CAP 4

Número mental: cheio após 4 pushes sem pop.

## 5. Invariantes

- 0 ≤ tail-head ≤ CAP
- slot = 2 + (index % CAP)
- FIFO

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| 5º push ok | não checou full |
| pop null cedo | head==tail errado |
| size -1 | stub |

## 7. Checklist

- [ ] 5º push false
- [ ] pop 10 depois 20

## Caderno de verificação — shared_atomics_ring

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. CAP=4.
2. head/tail.
3. FIFO 10→20.
4. full reject.
5. size=tail-head.

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
