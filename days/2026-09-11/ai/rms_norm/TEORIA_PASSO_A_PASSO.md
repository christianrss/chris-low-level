# Teoria passo a passo — RMSNorm estável em C

Laboratório em **C**. RMSNorm: `x / sqrt(mean(x^2)+eps)` e opcionalmente `* g`.

## 1. Trace Caso 1

```text
x = [3, 4]
mean(x^2) = (9+16)/2 = 12.5
rms = sqrt(12.5) ≈ 3.5355339
out = [3/rms, 4/rms]
com g=[2,2]: out *= 2
```

## 2. Por quê eps

Evita divisão por zero quando o vetor é ~0.

## 3. Por quê não LayerNorm completa

RMSNorm omite média centrada — mais barato; LLaMA usa variante.

## 4. Invariantes

- rms > 0 com eps>=0 e n>0
- escala g elemento a elemento

## 5. Bugs

| Sintoma | Causa |
|---------|-------|
| usou sum sem /n | esqueceu mean |
| g antes de norm | ordem errada |

## 6. Checklist

- [ ] sqrt(12.5)
- [ ] 3/rms e 4/rms

## Caderno de verificação — rms_norm

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. 12.5 mean sq.
2. rms≈3.5355.
3. divide.
4. g=2.
5. eps=0 no teste.

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

- Item de revisão 83: confirme o offset/valor do Caso 1 outra vez (revisão -17).
- Item de revisão 84: confirme o offset/valor do Caso 1 outra vez (revisão -16).
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
