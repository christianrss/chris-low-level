# Teoria passo a passo — PE import directory via Span (.NET)

Laboratório em **C#**. Continua o dia 08 (export RVA); agora o **data directory[1]** (Import).

## 1. O quê

`e_lfanew` em 0x3C aponta ao PE. Optional header PE32+ começa em pe+24. Data directories começam em opt+0x70 (PE32+)… neste lab usamos o mesmo layout do dia 08: dir[0] em opt+0x78, logo **dir[1] em opt+0x80** (opt+0x78+8).

## 2. Trace

```text
e_lfanew = 0x80
PE signature @ 0x80 = 'P''E'
opt = 0x80 + 4 + 20 = 0x98
import RVA @ 0x98 + 0x78 + 8 = 0x118 → valor 0x2000
```

## 3. Por quê Span

Evita copiar o PE inteiro; fatias `ReadOnlySpan<byte>` leem campos.

## 4. Por quê dir[1]

Export=0, Import=1, Resource=2 — o índice importa.

## 5. Invariantes

- MZ + PE válidos antes de ler RVA
- peOffset > 0 e dentro do buffer
- import RVA do fixture = 0x2000

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| leu 0x1000 | leu dir[0] export |
| offset 0 | não leu 0x3C |
| false MZ | length < 0x40 |

## 7. Checklist

- [ ] e_lfanew=0x80
- [ ] import @ 0x118 = 0x2000

## Caderno de verificação — pe_import_span

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. MZ em 0,1.
2. PE em 0x80.
3. opt=0x98.
4. dir1 @ 0x118.
5. RVA 0x2000.

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
