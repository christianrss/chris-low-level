# Teoria passo a passo — bump allocator com poison e canary

Laboratório em **C++**. Arena de **64 bytes**. Alocar `n` bytes reserva `n+1`: o extra é o canário `0xC3`.

## 1. O quê

Bump = ponteiro `used` que só sobe. `arena_reset` zera `used` e pinta o buffer com poison `0xA5`.

Por quê poison? Memória fresca com padrão conhecido revela use-after-reset.

## 2. Layout após alloc(8)

```text
índice: 0..7 payload, 8 = C3 canary, used = 9
```

## 3. Trace do teste

```text
reset → used=0, todos 0xA5
alloc(8) → p=&buf[0], used=9, buf[8]=0xC3
alloc(56) → nullptr porque 9+56+1=66 > 64
check(p,8) → 0; buf[8]=0 → check → -1
```

## 4. Por quê canário depois do payload

Overflow de 1 byte esmaga o canário antes do próximo objeto.

## 5. Invariantes

- used ≤ 64; alloc(0) → nullptr; canário em p[n].

## 6. Bugs comuns

| Sintoma | Causa |
|---------|-------|
| used=8 | esqueceu +1 |
| alloc(56) passa | sem +1 na conta |
| check -1 sempre | leu b[n-1] |

## 7. Lab vs produção

ASAN usa shadow; aqui 1 byte inline — mesmo porquê.

## 8. Por quê CAP 64

Força o Caso full com conta mental 8+1+56+1=66>64.

## 9. Checklist

- [ ] used após alloc(8) é 9
- [ ] poison 0xA5, canary 0xC3

## Caderno de verificação — bump_poison_arena

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. Poison 0xA5 em 64 bytes.
2. used=9 após n=8.
3. Canário em índice 8.
4. 66>64 rejeita.
5. check lê b[n].

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
