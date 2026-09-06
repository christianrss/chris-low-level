# Pesquisa guiada — Gzip member parse

Leia RFC 1952 (§2.3 member format) e compare com `tooling/zlib_gzip_containers`. Perguntas:

1. Por que bits 5–7 de FLG são reservados e devem ser zero?
2. Qual a diferença entre CRC32 do trailer e FHCRC (CRC16 do header)?
3. ISIZE é mod 2^32 — como isso afeta arquivos >4 GiB?
4. Por que FNAME é C-string e não length-prefixed?
5. Em que ponto o lab Node `gunzip_transform` esconde este layout?

## Regra

Entenda e valide; não cole implementação de crates `flate2`/`libz`. Registre decisões.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha) | | |

## Checkpoint

Monte no papel um header com `FLG=FNAME` e nome `a\0`. Calcule `deflate_start`. Só então faça `RS-GZ-02`.
