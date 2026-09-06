# Pesquisa guiada — CHRLE em Rust

Leia a RFC mental do lab C++ (`systems/rle_byte_codec/TEORIA`) e o capítulo de slices no Rust Book. Perguntas:

1. Por que `u32::from_le_bytes` é preferível a shifts manuais neste lab?
2. Qual diferença entre panic por OOB e retornar `RleError::Truncated`?
3. Por que o teto de run é 255 e não 256?
4. Como `&[u8]` se compara a `std::span<const uint8_t>` em C++20?
5. Quando você usaria `Cow<[u8]>` em vez de sempre alocar `Vec`?

## Regra

Use as fontes para **entender e validar**. Não copie o gabarito C++ byte a byte sem entender ownership. Registre o que aprendeu.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler) | | |

## Checkpoint

Escreva no papel o hex de `AAAAB` (magic + len + 2 runs). Só então implemente `RS-RLE-01`.
