# Teoria passo a passo — hazard_pointer_stack

Laboratório em **python** (trilha GitHub incorporada ao dia).

## 1. O quê

Stack com hazard pointer educacional (protect antes de deref).

## 2. Como

```text
entrada fixture/literal -> validacao -> TODO transform -> assert
```

## 3. Tabela de contrato

| Campo | Papel |
|-------|-------|
| starter | stubs TODO |
| solutions | PEDAGOGY-SOLUTION |
| teste | PEDAGOGY-TEST |

## 4. TODOs

| ID | Papel |
|----|-------|
| `D9-HP-PUSH` | assert do teste |
| `D9-HP-POP` | assert do teste |
| `D9-HP-PROTECT` | assert do teste |

## 5. Trace numerico

Use o Caso 1 do teste no papel antes de editar.

## 6. Por quê este lab

Por quê está neste dia? Complementa o core com um eixo classico (allocator/parser/agent/…).

## 7. Por quê falhar cedo

Por quê erro explicito? Evita default silencioso.

## 8. Por quê literais no teste

Por quê o assert fixa numeros? Reproduzibilidade sem adivinhar.

## 9. Invariantes

1. Determinismo
2. Bounds / estados ilegais rejeitados
3. Nao alterar o teste
4. Ordem dos TODOs

## 10. Bugs comuns

| Sintoma | Causa | Checagem |
|---------|-------|----------|
| off-by-one | indice | imprima cursor |
| estado sujo | sem reset | isole o caso |
| NaN/None | dominio | guarde eps |

## 11. Lab vs producao

Recorte pedagogico do mesmo problema real.

## 12. Checklist

- [ ] Caso 1 no papel
- [ ] Arquivo + funcao
- [ ] Sei o que nao mudar

## 13. Relacao com o core

Compare com o modulo core da mesma trilha neste dia quando houver sobreposicao tematica.

## Nota operacional 1 — hazard_pointer_stack

Detalhe 1: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 2 — hazard_pointer_stack

Detalhe 2: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 3 — hazard_pointer_stack

Detalhe 3: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 4 — hazard_pointer_stack

Detalhe 4: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 5 — hazard_pointer_stack

Detalhe 5: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 6 — hazard_pointer_stack

Detalhe 6: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 7 — hazard_pointer_stack

Detalhe 7: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 8 — hazard_pointer_stack

Detalhe 8: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 9 — hazard_pointer_stack

Detalhe 9: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 10 — hazard_pointer_stack

Detalhe 10: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 11 — hazard_pointer_stack

Detalhe 11: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 12 — hazard_pointer_stack

Detalhe 12: literal do Caso 1 nao e sinonimo do core vizinho.

## Nota operacional 13 — hazard_pointer_stack

Detalhe 13: literal do Caso 1 nao e sinonimo do core vizinho.
