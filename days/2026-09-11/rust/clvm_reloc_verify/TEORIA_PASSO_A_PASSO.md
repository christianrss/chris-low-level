# Teoria passo a passo — verificar tabela de reloc em Rust

Laboratório em **Rust**. A tabela é uma sequência de `u16` LE (sites). Antes de aplicar patches (lab C), valide bounds.

## 1. O quê

`reloc_table_len`: length par → N = len/2. Ímpar → Err.

## 2. Trace

```text
bytes = 02 00 04 00  → N=2
site[0]=2, site[1]=4
code_len=8 → 2+2<=8 e 4+2<=8 → Ok
site 0x0007 com code_len=8 → 7+2>8 → Err
```

## 3. Por quê Result

Panic OOB esconderia o contrato; `Err` é a falha esperada.

## 4. Por quê LE

Mesmo wire format do lab C `clvm_reloc_apply`.

## 5. Invariantes

- len%2==0
- site+2 <= code_len para todos
- index < N

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| Ok em ímpar | não checou %2 |
| site big-endian | from_be_bytes |
| 7 passa em len 8 | comparou site < len |

## 7. Checklist

- [ ] N=1 para 02 00
- [ ] site índice 1 = 4
- [ ] 7+2>8 falha

## Caderno de verificação — clvm_reloc_verify

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. Tabela par.
2. from_le_bytes.
3. site+2<=code_len.
4. Err em ímpar.
5. Cruzar com lab C.

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
