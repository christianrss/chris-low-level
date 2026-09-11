# Teoria passo a passo — gc_allocation_probe

Este laboratório veio da **trilha paralela GitHub** do dia 2026-09-08.

## 1. O quê

Sondas de alocacao .NET: new vs pool vs contagem.

## 2. Como — fluxo de dados

```text
entrada (fixture / literal do teste)
  -> validacao de limites
  -> transformacao do TODO
  -> saida comparada por igualdade estrita
```

## 3. Tabela de contrato

| Campo | Papel |
|-------|-------|
| starter | stubs com TODO |
| solutions | gabarito PEDAGOGY-SOLUTION |
| teste | PEDAGOGY-TEST / ctest / node / dotnet |

## 4. TODOs deste módulo

| ID | Papel |
|----|-------|
| `D6-DN-ALLOC` | contrato do assert correspondente |
| `D6-DN-NEW` | contrato do assert correspondente |
| `D6-DN-POOL` | contrato do assert correspondente |

## 5. Trace numerico (Caso 1)

Siga o Caso 1 de `TESTES_GUIADOS.md` / asserts do teste no papel **antes** de editar.
Nao invente outro exemplo: o runner compara o literal.

## 6. Por quê este lab existe

Por quê está no dia 08 junto do toolchain CLVM? Porque treina um eixo ortogonal
(concorrencia / cache / ranking / automata) sem substituir o fio ISA.

## 7. Por quê falhar cedo

Por quê retornar false/Err/-1 imediatamente? Porque valor default silencioso
propaga lixo para o proximo assert.

## 8. Por quê o teste fixa literais

Por quê literais em vez de "quase certo"? Para impedir solucoes que so funcionam
no exemplo inventado pelo aluno.

## 9. Invariantes

1. Determinismo: mesma entrada => mesma saida.
2. Limites de capacidade / OOB respeitados.
3. Nao alterar assinaturas nem o teste.
4. Ordem dos TODOs da RESOLUCAO.

## 10. Bugs comuns

| Sintoma | Causa | Checagem |
|---------|-------|----------|
| off-by-one | indice/size | imprima cursor |
| ordem errada | publica antes de gravar | barreira acquire/release |
| score/prob NaN | divisao / log dominio | guarde eps |
| flake | estado residual | reset entre casos |

## 11. Lab versus producao

Producao tem mais flags e formatos. Aqui o recorte cabe no papel e ainda rejeita
o bug classico do modulo.

## 12. Checklist

- [ ] Caso 1 no papel
- [ ] Arquivo + funcao do primeiro TODO
- [ ] Sei o que nao mudar

## 13. Relacao com o core do dia

Compare com o anel C (`input_event_ring_mux`), o softmax C (`softmax_stable`) ou o
wasm asm (`wasm_section_header`) quando o tema se sobrepoe — sao contratos diferentes.

## Nota operacional 1 — dotnet/gc_allocation_probe

Detalhe 1: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 1.

## Nota operacional 2 — dotnet/gc_allocation_probe

Detalhe 2: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 2.

## Nota operacional 3 — dotnet/gc_allocation_probe

Detalhe 3: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 3.

## Nota operacional 4 — dotnet/gc_allocation_probe

Detalhe 4: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 4.

## Nota operacional 5 — dotnet/gc_allocation_probe

Detalhe 5: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 5.

## Nota operacional 6 — dotnet/gc_allocation_probe

Detalhe 6: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 6.

## Nota operacional 7 — dotnet/gc_allocation_probe

Detalhe 7: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 7.

## Nota operacional 8 — dotnet/gc_allocation_probe

Detalhe 8: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 8.

## Nota operacional 9 — dotnet/gc_allocation_probe

Detalhe 9: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 9.

## Nota operacional 10 — dotnet/gc_allocation_probe

Detalhe 10: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 10.

## Nota operacional 11 — dotnet/gc_allocation_probe

Detalhe 11: o literal do Caso 1 deste modulo nao e intercambiavel com o do core CLVM. Confirme o assert antes do TODO passo 11.
