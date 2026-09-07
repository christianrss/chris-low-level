# N3 — operador `%` (ainda CLVM v1)

Extensão do subset **no capstone** `projects/chris-vm` (não no Dia 01).

## O que foi feito

- Lexer: token `%`
- Parser: mesma precedência que `*`/`/`
- Codegen: `a % b` → `a - (a/b)*b`
- Golden: `examples/js/mod.js` → stdout `2`
- Teste: `integration_test.py` no chris-vm

## Exercício mental

Por que não adicionar opcode `MOD` agora? (Resposta: manter v1 estável; desugar ensina que HLL ≠ ISA 1:1.)

## Ligação

Labs N1 (codegen) / N2 (verifier) → depois desta extensão → N4 (FORMAT v2 strings).
