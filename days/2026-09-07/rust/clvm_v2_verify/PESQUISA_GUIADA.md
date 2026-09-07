# Pesquisa guiada — CLVM v2 Rust

Leia o wire format Python (`systems/clvm_v2_strings`) e a seção de slices do Rust Book. Perguntas:

1. Por que `wrapping_mul` no FNV em vez de `* as u32`?
2. Qual diferença entre `parse_image` retornar `ClvmV2Image` e expor só slices `&[u8]`?
3. Como `verify_stack` se compara ao verifier Python do Dia 07?
4. Por que o checksum inclui o pool e não só o code?
5. Quando você usaria `Cow<str>` no pool em vez de `String`?

## Regra

Use fontes para **entender e validar**. Registre decisões no código.

## Registro do aluno

| Pergunta | Resposta (3–5 linhas) | Decisão no código |
|----------|----------------------|-------------------|
| (preencha) | | |

## Checkpoint

Escreva no papel o hex de `hello_v2.clvm` (30 bytes). Só então implemente `CLVM-RS-V2-HEADER-01`.
