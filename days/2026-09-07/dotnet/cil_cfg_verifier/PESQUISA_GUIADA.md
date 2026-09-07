# Pesquisa guiada — CIL CFG

## Fontes primárias / técnicas

- ECMA-335 — partition III (CIL instruction set).
- Documentação Microsoft `System.Reflection.Emit.OpCodes`.
- PEVerify / artigos sobre **verifiable IL**.

## Perguntas antes de implementar

1. Como `br.s` calcula o target a partir do operando sbyte?
2. Por que um join point exige **mesma** stack depth (e tipos no verifier real)?
3. Diferença entre verificação linear e worklist fixpoint?
4. O que acontece se branch cai no meio de `ldc.i4`?

## Investigação prática

1. `ildasm` ou `dotnet` disassembly de método simples — compare offsets com seu decoder.
2. Construa IL manual byte-a-byte para método ok do teste; confira hex.
3. Leia descrição de `brtrue.s` na ECMA — confirme pops=1.

## Depois da implementação

Liste simplificações do subset, invariante de merge e métrica (ex.: max stack depth vs limite do método).
