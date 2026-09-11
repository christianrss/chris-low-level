# Teoria passo a passo — parse de uevent KEY=value

Laboratório em **C**. Kernel netlink uevent envia linhas `KEY=value` separadas por `\n`.

## 1. O quê

Uma linha `ACTION=add` vira chave `ACTION` e valor `add`. Sem `=` ou chave vazia → erro.

## 2. Trace (Caso 1)

```text
linha: ACTION=add
eq em offset 6
key = bytes [0..5) = ACTION
val = add
```

## 3. Bloco (Caso 2)

```text
ACTION=add\nDEVNAME=sda\n  →  n=2
```

## 4. Lookup (Caso 3)

`uevent_get(..., "DEVNAME")` → `"sda"`; chave ausente → NULL.

## 5. Por quê não JSON

Uevent histórico é texto plano KEY=value; parsers devem rejeitar malformação cedo.

## 6. Invariantes

- key e val cabem em 31/63 chars + NUL
- ordem das linhas = ordem na tabela
- get é busca linear

## 7. Bugs

| Sintoma | Causa |
|---------|-------|
| aceita `=x` | não rejeitou chave vazia |
| n=1 | não avançou após `\n` |
| get erra | strcmp invertido |

## 8. Por quê buffers fixos

Evita malloc no caminho de hotplug educacional.

## 9. Checklist

- [ ] ACTION=add → key/val corretos
- [ ] n==2 no bloco
- [ ] MISSING → NULL

## Caderno de verificação — uevent_kv_parse

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. Offset do '=' em ACTION=add é 6.
2. Duas linhas → n=2.
3. DEVNAME=sda.
4. Rejeitar =x.
5. NULL em MISSING.

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
