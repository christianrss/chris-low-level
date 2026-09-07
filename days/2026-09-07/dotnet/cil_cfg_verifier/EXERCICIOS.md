# Exercícios — CIL CFG verifier

## Fácil — desenhar CFG (`D5-CIL-DECODE`)

**Enunciado:** Para IL `ldc.i4 1; brtrue.s +5; ldc.i4 2; ret`, marque offsets de cada instrução e setas de successor.

**Arquivo-alvo:** caderno; valide offsets com decode.

**Critério de aceite:** identifique target do branch e fallthrough; `brtrue` tem dois successors.

## Médio — implementar decode (`D5-CIL-DECODE`)

**Enunciado:** Decodifique os cinco opcodes do subset. Rejeite opcode desconhecido e immediate truncado.

**Arquivo-alvo:** `starter/Chris.CilCfg/Verifier.cs`.

**Critério de aceite:** dicionário `ins` cobre método ok nos offsets 0,6,12,13.

## Difícil — worklist + merge (`D5-CIL-WORKLIST`, `D5-CIL-MERGE`)

**Enunciado:** Propague depth desde 0; falhe underflow e merge incompatible. Explique por que método bad falha.

**Arquivo-alvo:** `starter/Chris.CilCfg/Verifier.cs`.

**Critério de aceite:** ok retorna 2; bad lança `InvalidDataException`.

## Desafio — rastrear tipos

**Enunciado:** Esboce substituir `int depth` por stack de strings (`"i4"`) para `ldc.i4`/`add`. Quais opcodes quebram primeiro?

**Arquivo-alvo:** design doc local (sem alterar testes).

**Critério de aceite:** lista 3 regras ECMA que o subset atual ignora.
